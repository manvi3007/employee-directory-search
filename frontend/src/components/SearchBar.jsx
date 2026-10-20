import { Search, X } from "lucide-react";

export default function SearchBar({ value, onChange, disabled = false }) {
  return (
    <div className="search-bar">
      <Search size={20} aria-hidden="true" />

      <input
        type="search"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Search by employee name or department..."
        aria-label="Search employees by name or department"
        maxLength={100}
        disabled={disabled}
      />

      {value && (
        <button
          type="button"
          className="clear-button"
          onClick={() => onChange("")}
          aria-label="Clear search"
          disabled={disabled}
        >
          <X size={18} />
        </button>
      )}
    </div>
  );
}
