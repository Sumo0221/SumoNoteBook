/**
 * SumoNoteBook RAG Query Script
 * 
 * Performs semantic search on the SumoNoteBook LanceDB index.
 * 
 * Usage: node query_notebook.mjs "your query here" [--top N] [--json]
 */

import { connect } from "@lancedb/lancedb";
import OpenAI from "openai";

// ============================================================================
// Configuration (must match ingest_notebook.mjs)
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
  vectorDim: 1024,
  defaultTopK: 5,
};

// ============================================================================
// Query Engine
// ============================================================================

class NotebookRAG {
  constructor() {
    this.client = new OpenAI({
      apiKey: CONFIG.ollama.apiKey,
      baseURL: CONFIG.ollama.baseURL,
    });
    this.db = null;
    this.table = null;
  }
  
  async connect() {
    if (!this.db) {
      this.db = await connect(CONFIG.lancedb.dbPath);
    }
    const names = await this.db.tableNames();
    if (!names.includes(CONFIG.lancedb.tableName)) {
      throw new Error(`Table '${CONFIG.lancedb.tableName}' not found. Run ingest first.`);
    }
    if (!this.table) {
      this.table = await this.db.openTable(CONFIG.lancedb.tableName);
    }
    return this.table;
  }
  
  async embedQuery(text) {
    const response = await this.client.embeddings.create({
      model: CONFIG.ollama.model,
      input: text,
      encoding_format: "float",
    });
    return response.data[0].embedding;
  }
  
  async query(queryText, topK = CONFIG.defaultTopK) {
    await this.connect();
    
    console.error(`Querying: "${queryText}"`);
    
    // Embed the query
    const queryVector = await this.embedQuery(queryText);
    
    if (!queryVector || queryVector.length !== CONFIG.vectorDim) {
      throw new Error(`Invalid query embedding: ${queryVector?.length} dims`);
    }
    
    // Search LanceDB - use correct LanceDB JS API: vectorSearch(vec).distanceType().limit().toArray()
    const results = await this.table
      .vectorSearch(queryVector)
      .distanceType("cosine")
      .limit(topK)
      .toArray();
    
    return results;
  }
}

// ============================================================================
// CLI
// ============================================================================

async function main() {
  const args = process.argv.slice(2);
  
  if (args.includes("--help") || args.includes("-h") || args.length === 0) {
    console.log("Usage: node query_notebook.mjs \"your query\" [--top N] [--json]");
    console.log("  --top N   Return top N results (default: 5)");
    console.log("  --json    Output as JSON");
    console.log("  --help    Show this help");
    process.exit(0);
  }
  
  const topArg = args.find(a => a.startsWith("--top="));
  const topK = topArg ? parseInt(topArg.split("=")[1]) : CONFIG.defaultTopK;
  const asJson = args.includes("--json");
  const queryText = args.filter(a => !a.startsWith("--"))[0] || "";
  
  if (!queryText) {
    console.error("Error: No query text provided");
    process.exit(1);
  }
  
  const rag = new NotebookRAG();
  
  try {
    const results = await rag.query(queryText, topK);
    
    if (asJson) {
      console.log(JSON.stringify(results, null, 2));
    } else {
      console.log("\n" + "=".repeat(60));
      console.log(`TOP ${results.length} RESULTS`);
      console.log("=".repeat(60));
      
      results.forEach((r, i) => {
        // LanceDB returns _distance (cosine distance), lower = more similar
        // Convert to similarity score: 1 - distance (0-1 scale, higher = better)
        const distance = r._distance ?? r._score ?? 0;
        const score = (1 - distance).toFixed(4);
        console.log(`\n[${i + 1}] ${r.source_file} (chunk ${r.chunk_index}) [score: ${score}]`);
        console.log("-".repeat(50));
        const preview = r.text.length > 300 ? r.text.slice(0, 300) + "..." : r.text;
        console.log(preview);
      });
    }
  } catch (e) {
    console.error(`Error: ${e.message}`);
    process.exit(1);
  }
}

main();
