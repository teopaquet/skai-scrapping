import express from "express";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const app = express();
const PORT = 3001;

app.use(express.json({ limit: '20mb' }));

// Pour __dirname en ES module
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Endpoint pour sauvegarder le CSV
app.post("/api/save-linkedin-csv", (req, res) => {
  const { rows } = req.body;
  if (!Array.isArray(rows)) {
    return res.status(400).json({ error: "Rows must be an array" });
  }
  // Génère le CSV
  const header = "company_name,linkedin_url,description,fleet_size";
  const csv = [
    header,
    ...rows.map(row => {
      // Échappe les virgules et guillemets
      return [row.company_name, row.linkedin_url, row.description, row.fleet_size]
        .map(val => {
          if (val == null) return "";
          const str = String(val).replace(/"/g, '""');
          return str.includes(",") || str.includes("\n") ? `"${str}"` : str;
        })
        .join(",");
    })
  ].join("\n");

  // Chemin absolu vers le CSV
  const csvPath = path.join(__dirname, "..", "public", "linkedin_list_merged_with_fleet.csv");
  fs.writeFile(csvPath, csv, "utf8", err => {
    if (err) {
      return res.status(500).json({ error: "Erreur lors de la sauvegarde du CSV" });
    }
    res.json({ success: true });
  });
});

app.listen(PORT, () => {
  console.log(`API backend running on http://localhost:${PORT}`);
});
