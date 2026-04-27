import { connect } from "@lancedb/lancedb";
(async () => {
  const db = await connect('C:\\Users\\rayray\\.openclaw\\memory\\lancedb-pro');
  const names = await db.tableNames();
  console.log('Tables:', names);
  if (names.includes('sumo_notebook')) {
    const tbl = await db.openTable('sumo_notebook');
    const schema = await tbl.schema();
    console.log('Schema:', JSON.stringify(schema, null, 2));
    const count = await tbl.countRows();
    console.log('Row count:', count);
    const sample = await tbl.query().limit(1).toArray();
    console.log('Sample row keys:', Object.keys(sample[0] || {}));
    console.log('Sample row:', JSON.stringify(sample[0], null, 2));
  }
})();
