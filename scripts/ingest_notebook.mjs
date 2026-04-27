/**
 * SumoNoteBook RAG Ingestion Script v2
 * 
 * Uses OpenAI SDK (same as memory-lancedb-pro plugin) for reliable API calls.
 * 
 * Usage: node ingest_notebook.mjs [--rebuild] [--limit N]
 */

import { join as pathJoin, relative as pathRelative } from "node:path";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { randomUUID } from "node:crypto";
import { connect } from "@lancedb/lancedb";
import OpenAI from "openai";

// ============================================================================
// Configuration
// ============================================================================

const CONFIG = {
  ollama: {
    baseURL: "http://localhost:11434/v1",
    model: "qwen3-embedding:0.6b",
    apiKey: "ollama",
  },
  lancedb: {
    dbPath: "C:\\Users\\rayray\\.openclaw\\memory\\lancedb-pro",
    tableName: "sumo_notebook",
  },
  notebookPath: "C:\\butler_sumo\\library\\SumoNoteBook",
  chunking: {
    maxChunkSize: 1500,   // Conservative: stay well under 2048 token context
    overlapSize: 100,
    minChunkSize: 80,
  },
  embedBatchSize: 4,       // Process fewer at a time to avoid batch context overflow
  vectorDim: 1024,
};

// ============================================================================
// Text Sanitization
// ============================================================================

function sanitizeText(text) {
  if (!text) return "";
  return text
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n")
    .replace(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/g, "")
    .replace(/\t/g, " ")
    .replace(/\u200B/g, "")
    .replace(/\u3000/g, " ")
    .replace(/  +/g, " ")
    .trim();
}

// ============================================================================
// Text Chunking
// ============================================================================

function chunkText(text, config = CONFIG.chunking) {
  const { maxChunkSize, overlapSize, minChunkSize } = config;
  const chunks = [];
  const metadatas = [];
  
  if (!text || text.trim().length === 0) {
    return { chunks: [], metadatas: [] };
  }
  
  const SENTENCE_ENDING = /[.!?。！？\n]/;
  let pos = 0;
  const totalLen = text.length;
  
  while (pos < totalLen) {
    const remaining = totalLen - pos;
    
    if (remaining <= maxChunkSize) {
      const chunk = text.slice(pos).trim();
      if (chunk.length >= minChunkSize) {
        chunks.push(chunk);
        metadatas.push({ startIndex: pos, endIndex: totalLen, length: chunk.length });
      }
      break;
    }
    
    let end = Math.min(pos + maxChunkSize, totalLen);
    let splitFound = false;
    
    for (let i = end - 1; i >= Math.max(pos + Math.floor(maxChunkSize * 0.65), pos + minChunkSize); i--) {
      if (SENTENCE_ENDING.test(text[i])) {
        end = i + 1;
        splitFound = true;
        break;
      }
    }
    
    if (!splitFound) {
      for (let i = end - 1; i >= Math.max(pos + Math.floor(maxChunkSize * 0.65), pos + minChunkSize); i--) {
        if (text[i] === "\n") {
          end = i + 1;
          splitFound = true;
          break;
        }
      }
    }
    
    if (!splitFound) {
      for (let i = end - 1; i >= Math.max(pos + Math.floor(maxChunkSize * 0.65), pos + minChunkSize); i--) {
        if (/\s/.test(text[i])) {
          end = i;
          splitFound = true;
          break;
        }
      }
    }
    
    const chunk = text.slice(pos, end).trim();
    if (chunk.length >= minChunkSize) {
      chunks.push(chunk);
      metadatas.push({ startIndex: pos, endIndex: end, length: chunk.length });
    }
    
    pos = Math.max(end - overlapSize, pos + Math.floor(maxChunkSize * 0.5));
  }
  
  return { chunks, metadatas };
}

// ============================================================================
// Ollama Embedding via OpenAI SDK
// ============================================================================

async function createEmbedder() {
  const client = new OpenAI({
    apiKey: CONFIG.ollama.apiKey,
    baseURL: CONFIG.ollama.baseURL,
  });
  
  async function embedSingle(text) {
    const sanitized = sanitizeText(text);
    if (!sanitized) return null;
    
    const response = await client.embeddings.create({
      model: CONFIG.ollama.model,
      input: sanitized,
      encoding_format: "float",
    });
    
    const embedding = response.data?.[0]?.embedding;
    if (!embedding || !Array.isArray(embedding)) return null;
    if (embedding.length !== CONFIG.vectorDim) {
      console.warn(`  Dim mismatch: ${embedding.length} vs ${CONFIG.vectorDim}`);
      return null;
    }
    return embedding;
  }
  
  async function embedBatch(texts) {
    const sanitized = texts.map(sanitizeText).filter(t => t.length > 0);
    if (sanitized.length === 0) return texts.map(() => null);
    
    const response = await client.embeddings.create({
      model: CONFIG.ollama.model,
      input: sanitized,
      encoding_format: "float",
    });
    
    const results = new Array(texts.length).fill(null);
    for (const item of response.data) {
      const embedding = item.embedding;
      if (embedding && Array.isArray(embedding) && embedding.length === CONFIG.vectorDim) {
        results[item.index] = embedding;
      }
    }
    return results;
  }
  
  return { embedSingle, embedBatch, client };
}

// ============================================================================
// File Scanner
// ============================================================================

function scanMarkdownFiles(dirPath, basePath = dirPath) {
  const files = [];
  
  function walk(dir) {
    try {
      const entries = readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        if (entry.name.startsWith(".") || entry.name === "node_modules") continue;
        
        const fullPath = pathJoin(dir, entry.name);
        
        if (entry.isDirectory()) {
          walk(fullPath);
        } else if (entry.isFile() && entry.name.endsWith(".md")) {
          try {
            const stat = statSync(fullPath);
            const relPath = pathRelative(basePath, fullPath).replace(/\\/g, "/");
            files.push({ fullPath, relPath, size: stat.size, mtime: stat.mtime });
          } catch (e) {
            // skip
          }
        }
      }
    } catch (e) {
      // skip inaccessible dirs
    }
  }
  
  walk(dirPath);
  return files;
}

// ============================================================================
// Progress Bar
// ============================================================================

function progressBar(current, total, width = 30) {
  const pct = Math.round((current / total) * 100);
  const filled = Math.round((current / total) * width);
  const bar = "█".repeat(filled) + "░".repeat(width - filled);
  return `[${bar}] ${current}/${total} (${pct}%)`;
}

// ============================================================================
// Main
// ============================================================================

async function ingestNotebook(rebuild = false) {
  const startTime = Date.now();
  
  console.log("=".repeat(60));
  console.log("SumoNoteBook RAG Ingestion v2 (OpenAI SDK)");
  console.log("=".repeat(60));
  console.log(`Ollama: ${CONFIG.ollama.baseURL} / ${CONFIG.ollama.model}`);
  console.log(`LanceDB: ${CONFIG.lancedb.dbPath}`);
  console.log(`Notebook: ${CONFIG.notebookPath}`);
  console.log(`Mode: ${rebuild ? "REBUILD" : "INCREMENTAL"}`);
  console.log("");
  
  // Connect to LanceDB
  console.log("[1/5] Connecting to LanceDB...");
  let db;
  try {
    db = await connect(CONFIG.lancedb.dbPath);
    console.log("  ✓ Connected");
  } catch (e) {
    console.error(`  ✗ Failed: ${e.message}`);
    process.exit(1);
  }
  
  if (rebuild) {
    console.log("\n[REBUILD] Dropping existing table...");
    try {
      const tableNames = await db.tableNames();
      if (tableNames.includes(CONFIG.lancedb.tableName)) {
        await db.dropTable(CONFIG.lancedb.tableName);
        console.log("  ✓ Dropped");
      }
    } catch (e) {
      console.warn(`  Drop warning: ${e.message}`);
    }
  }
  
  // Scan files
  console.log("\n[2/5] Scanning Markdown files...");
  const mdFiles = scanMarkdownFiles(CONFIG.notebookPath).filter(f => f.fullPath.endsWith(".md"));
  console.log(`  Found ${mdFiles.length} .md files`);
  
  if (mdFiles.length === 0) {
    console.error("  ✗ No markdown files found!");
    process.exit(1);
  }
  
  // Read and chunk
  console.log("\n[3/5] Reading and chunking...");
  const allChunks = [];
  let totalChars = 0;
  
  for (let i = 0; i < mdFiles.length; i++) {
    const file = mdFiles[i];
    process.stdout.write(`\r  [${i + 1}/${mdFiles.length}] ${file.relPath}`);
    
    try {
      const content = readFileSync(file.fullPath, "utf-8");
      const { chunks, metadatas } = chunkText(content);
      totalChars += content.length;
      
      for (let j = 0; j < chunks.length; j++) {
        allChunks.push({
          id: randomUUID(),
          text: chunks[j],
          source_file: file.relPath,
          chunk_index: j,
          chunk_start: metadatas[j]?.startIndex || 0,
          chunk_end: metadatas[j]?.endIndex || 0,
        });
      }
    } catch (e) {
      // skip problematic files
    }
  }
  
  console.log(`\n\n  Total chunks: ${allChunks.length}`);
  console.log(`  Total chars: ${(totalChars / 1024).toFixed(1)} KB`);
  
  if (allChunks.length === 0) {
    console.error("  ✗ No chunks generated!");
    process.exit(1);
  }
  
  // Create embedder
  console.log("\n[4/5] Testing Ollama connection...");
  let embedder;
  try {
    embedder = await createEmbedder();
    const test = await embedder.embedSingle("test");
    if (test && test.length === CONFIG.vectorDim) {
      console.log(`  ✓ Ollama working (768-dim)`);
    } else {
      throw new Error(`Unexpected embedding dim: ${test?.length}`);
    }
  } catch (e) {
    console.error(`  ✗ Ollama error: ${e.message}`);
    process.exit(1);
  }
  
  // Embed all chunks
  console.log("\n[5/5] Embedding chunks...");
  let completed = 0;
  let failed = 0;
  
  for (let i = 0; i < allChunks.length; i += CONFIG.embedBatchSize) {
    const batch = allChunks.slice(i, i + CONFIG.embedBatchSize);
    const texts = batch.map(c => c.text);
    
    try {
      const vectors = await embedder.embedBatch(texts);
      for (let j = 0; j < vectors.length; j++) {
        if (vectors[j] && vectors[j].length === CONFIG.vectorDim) {
          allChunks[i + j].vector = vectors[j];
          completed++;
        } else {
          failed++;
        }
      }
    } catch (e) {
      console.error(`\n  Batch error at ${i}: ${e.message}`);
      failed += batch.length;
    }
    
    process.stdout.write(`\r  ${progressBar(Math.min(i + CONFIG.embedBatchSize, allChunks.length), allChunks.length)}`);
    
    await new Promise(r => setTimeout(r, 30));
  }
  
  console.log(`\n\n  ✓ Embedded: ${completed}  ⚠ Failed: ${failed}`);
  
  const validChunks = allChunks.filter(c => c.vector && c.vector.length === CONFIG.vectorDim);
  if (validChunks.length === 0) {
    console.error("  ✗ No valid chunks to store!");
    process.exit(1);
  }
  
  // Store to LanceDB
  console.log("\n[STORE] Writing to LanceDB...");
  try {
    const tableNames = await db.tableNames();
    
    if (tableNames.includes(CONFIG.lancedb.tableName)) {
      const table = await db.openTable(CONFIG.lancedb.tableName);
      const records = validChunks.map(c => ({
        id: c.id,
        text: c.text,
        source_file: c.source_file,
        chunk_index: c.chunk_index,
        chunk_start: c.chunk_start,
        chunk_end: c.chunk_end,
        vector: c.vector,
      }));
      await table.add(records);
    } else {
      // Create table with initial record to define schema (including 768-dim vector)
      const initialRecord = {
        id: validChunks[0].id,
        text: validChunks[0].text,
        source_file: validChunks[0].source_file,
        chunk_index: validChunks[0].chunk_index,
        chunk_start: validChunks[0].chunk_start,
        chunk_end: validChunks[0].chunk_end,
        vector: validChunks[0].vector,
      };
      const table = await db.createTable(CONFIG.lancedb.tableName, [initialRecord]);
      
      // Add remaining records (skip first since it was used for schema)
      if (validChunks.length > 1) {
        const remaining = validChunks.slice(1).map(c => ({
          id: c.id,
          text: c.text,
          source_file: c.source_file,
          chunk_index: c.chunk_index,
          chunk_start: c.chunk_start,
          chunk_end: c.chunk_end,
          vector: c.vector,
        }));
        await table.add(remaining);
      }
    }
    console.log("  ✓ Stored");
  } catch (e) {
    console.error(`  ✗ LanceDB error: ${e.message}`);
    console.error(e.stack);
    process.exit(1);
  }
  
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log("\n" + "=".repeat(60));
  console.log("INGESTION COMPLETE");
  console.log("=".repeat(60));
  console.log(`  Files: ${mdFiles.length}`);
  console.log(`  Chunks: ${validChunks.length}`);
  console.log(`  Time: ${elapsed}s`);
  if (parseFloat(elapsed) > 0) {
    console.log(`  Speed: ${(validChunks.length / parseFloat(elapsed)).toFixed(1)} chunks/s`);
  }
}

// ============================================================================
// CLI
// ============================================================================

const args = process.argv.slice(2);
const rebuild = args.includes("--rebuild");
const help = args.includes("--help") || args.includes("-h");

if (help) {
  console.log("Usage: node ingest_notebook.mjs [options]");
  console.log("  --rebuild   Drop and recreate table");
  console.log("  --help      Show this help");
  process.exit(0);
}

ingestNotebook(rebuild).catch(e => {
  console.error("Fatal:", e.message);
  process.exit(1);
});
