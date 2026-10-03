export interface Transaction {
  id?: number
  date: string
  description: string
  amount: number
  type: "debit" | "credit"
  category?: string | null
  ai_confidence?: number | null
  categorization_source?: string | null
}

export interface ImportResponse {
  message: string
  transactions_imported: number
  transactions: Transaction[]
}


const API_URL = "http://127.0.0.1:8000"


export async function importStatement(
  file: File
): Promise<ImportResponse> {
  const formData = new FormData()

  formData.append("file", file)

  const response = await fetch(
    `${API_URL}/transactions/import`,
    {
      method: "POST",
      body: formData,
    }
  )

  if (!response.ok) {
    const error = await response.json()

    throw new Error(
      error.detail || "Failed to import statement."
    )
  }

  return response.json()
}


export async function getTransactions(): Promise<Transaction[]> {
  const response = await fetch(
    `${API_URL}/transactions/`
  )

  if (!response.ok) {
    throw new Error(
      "Failed to fetch transactions."
    )
  }

  return response.json()
}