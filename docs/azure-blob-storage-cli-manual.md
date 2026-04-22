# Azure Blob Storage Administration Manual (Azure CLI + Azurite)

This document explains how to manage **containers and blobs** using the **Azure CLI**.

The commands work in two environments:

- **Azurite (local emulator)**
- **Azure Blob Storage (cloud service)**

Examples for both environments are included.

This manual is useful for testing the ingestion pipeline defined in:

```
docs/implementation/mvp-milestone-01-ingestion.md
```

Where PDFs are stored in **Blob Storage** before being processed by the ingestion service.

---

# 1. Concepts

Azure Blob Storage has a simple hierarchy:

```
Storage Account
    ↓
Container
    ↓
Blob
```

Example:

```
eduweaverstorage
   └── documents
         ├── drilling-paper.pdf
         └── bop-control-procedures.pdf
```

Terminology:

- **Storage Account** → top-level Azure resource
- **Container** → similar to a bucket
- **Blob** → stored file (PDF, image, JSON, etc.)

---

# 2. Using Azurite (Local Development)

Azurite is a **local emulator for Azure Storage**.

Typical ports:

```
Blob service: 10000
Queue service: 10001
Table service: 10002
```

Default development connection string:

```
UseDevelopmentStorage=true
```

This allows Azure CLI to interact with Azurite.

---

# 3. List Containers

## Azurite

```
az storage container list \
  --connection-string "UseDevelopmentStorage=true"
```

Example output:

```
[
  {
    "name": "documents"
  }
]
```

---

## Azure Cloud

```
az storage container list \
  --account-name <storage_account>
```

Example:

```
az storage container list \
  --account-name eduweaverstorage
```

---

# 4. Create a Container

## Azurite

```
az storage container create \
  --name documents \
  --connection-string "UseDevelopmentStorage=true"
```

---

## Azure Cloud

```
az storage container create \
  --name documents \
  --account-name eduweaverstorage
```

---

# 5. List Blobs in a Container

## Azurite

```
az storage blob list \
  --container-name documents \
  --connection-string "UseDevelopmentStorage=true"
```

Example output:

```
[
  {
    "name": "bop-control-procedures.pdf"
  },
  {
    "name": "drilling-paper.pdf"
  }
]
```

---

## Azure Cloud

```
az storage blob list \
  --container-name documents \
  --account-name eduweaverstorage
```

---

# 6. Upload a File (Blob)

## Azurite

```
az storage blob upload \
  --container-name documents \
  --name drilling-paper.pdf \
  --file ./resources/drilling-paper.pdf \
  --connection-string "UseDevelopmentStorage=true"
```

---

## Azure Cloud

```
az storage blob upload \
  --container-name documents \
  --name drilling-paper.pdf \
  --file ./resources/drilling-paper.pdf \
  --account-name eduweaverstorage
```

---

# 7. Download a Blob

## Azurite

```
az storage blob download \
  --container-name documents \
  --name drilling-paper.pdf \
  --file ./downloaded.pdf \
  --connection-string "UseDevelopmentStorage=true"
```

---

## Azure Cloud

```
az storage blob download \
  --container-name documents \
  --name drilling-paper.pdf \
  --file ./downloaded.pdf \
  --account-name eduweaverstorage
```

---

# 8. Delete a Blob

## Azurite

```
az storage blob delete \
  --container-name documents \
  --name drilling-paper.pdf \
  --connection-string "UseDevelopmentStorage=true"
```

---

## Azure Cloud

```
az storage blob delete \
  --container-name documents \
  --name drilling-paper.pdf \
  --account-name eduweaverstorage
```

---

# 9. Delete a Container

## Azurite

```
az storage container delete \
  --name documents \
  --connection-string "UseDevelopmentStorage=true"
```

---

## Azure Cloud

```
az storage container delete \
  --name documents \
  --account-name eduweaverstorage
```

---

# 10. Useful Debug Commands

Show storage accounts:

```
az storage account list
```

Check container existence:

```
az storage container exists \
  --name documents
```

Show blob metadata:

```
az storage blob show \
  --container-name documents \
  --name drilling-paper.pdf
```

---

# 11. Typical Workflow for the Ingestion Pipeline

Example flow used by the EduWeaver ingestion service.

1. Upload PDF to storage

```
az storage blob upload \
  --container-name documents \
  --name paper.pdf \
  --file ./paper.pdf \
  --connection-string "UseDevelopmentStorage=true"
```

2. Verify blob exists

```
az storage blob list \
  --container-name documents \
  --connection-string "UseDevelopmentStorage=true"
```

3. Run ingestion pipeline

```
DoclingEngine.extract("paper.pdf")
```

The ingestion service downloads the blob using:

```
download_blob_stream()
```

and passes the stream to the Docling parser.

---

# 12. Recommended Folder Structure

For this project the container layout could be:

```
documents
   ├── raw/
   │     paper1.pdf
   │     paper2.pdf
   │
   ├── normalized/
   │     normalized_document.json
   │
   └── chunks/
         chunks.json
```

This keeps raw inputs separated from generated artifacts.

---

# 13. Summary

Azure CLI allows full management of blob storage.

Key commands:

```
container list
container create
blob upload
blob list
blob download
blob delete
```

During development:

```
UseDevelopmentStorage=true
```

connects Azure CLI to **Azurite**.

When deployed to Azure, commands remain almost identical, only replacing the connection string with the **storage account name**.
