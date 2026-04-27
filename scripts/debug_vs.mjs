import { connect } from "@lancedb/lancedb";
import OpenAI from "openai";

const CONFIG = {
  ollama: {
    baseURL: "http://localhost:11434/v1",
    model: "nomic-embed-text",
    apiKey: "ollama",
  },
  lancedb: {
    dbPath: "C:\\Users\\rayray\\.openclaw\\memory\\lancedb-pro",
    tableName: "sumo_notebook",
  },
  vectorDim: 768,
};

(async () => {
  const client = new OpenAI({
    apiKey: CONFIG.ollama.apiKey,
    baseURL: CONFIG.ollama.baseURL,
  });

  const db = await connect(CONFIG.lancedb.dbPath);
  const tbl = await db.openTable(CONFIG.lancedb.tableName);

  // Embed a query
  const resp = await client.embeddings.create({
    model: CONFIG.ollama.model,
    input: "演算法 資料結構",
    encoding_format: "float",
  });
  const queryVec = resp.data[0].embedding;
  console.log("Query vector dims:", queryVec.length);

  // Try vector search
  const results = await tbl
    .vectorSearch(queryVec)
    .distanceType("cosine")
    .limit(3)
    .toArray();

  console.log("Result keys:", Object.keys(results[0] || {}));
  console.log("Result[0]:", JSON.stringify(results[0], null, 2));
  console.log("_score in result?", "_score" in (results[0] || {}));
  console.log("_distance in result?", "_distance" in (results[0] || {}));
  console.log("All result keys across results:", results.map(r => Object.keys(r)));
})();
