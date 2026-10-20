const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function searchEmployees(search, signal) {
  if (!API_BASE_URL) {
    throw new Error("API configuration is missing.");
  }

  const url = new URL(`${API_BASE_URL.replace(/\/+$/, "")}/employees`);

  url.searchParams.set("search", search);

  const response = await fetch(url, { signal });

  if (!response.ok) {
    if (response.status === 422) {
      throw new Error("Please enter a search term of 100 characters or fewer.");
    }

    if (response.status === 503) {
      throw new Error(
        "Employee search is temporarily unavailable. Please try again.",
      );
    }

    throw new Error("Unable to load employees. Please try again.");
  }

  return response.json();
}
