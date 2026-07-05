import { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search } from 'lucide-react';
import { useAuth } from '../../../context/AuthContext';
import "./SearchBar.css"

interface SearchResult {
  type: 'case' | 'evidence';
  id: string;
  label: string;
  title: string;
  case_id?: string;
}

const DEBOUNCE_MS = 300;

function SearchBar() {
  const { getAccessToken } = useAuth();
  const navigate = useNavigate();

  const [query, setQuery] = useState('');
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isSearching, setIsSearching] = useState(false);

  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  // Guards against an older, slower request overwriting a newer result set
  // if responses arrive out of order.
  const latestQueryRef = useRef('');

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);

    const trimmed = query.trim();
    if (trimmed.length === 0) {
      setResults([]);
      setIsOpen(false);
      return;
    }

    debounceRef.current = setTimeout(async () => {
      latestQueryRef.current = trimmed;
      setIsSearching(true);
      try {
        const token = await getAccessToken();
        const res = await fetch(`/api/search/?q=${encodeURIComponent(trimmed)}`, {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
          credentials: 'include',
        });
        if (!res.ok) return;

        const data: SearchResult[] = await res.json();
        // Only apply results if this is still the most recent query fired.
        if (latestQueryRef.current === trimmed) {
          setResults(data);
          setIsOpen(true);
        }
      } catch {
        // Silently drop — a failed search shouldn't disrupt the rest of the UI.
      } finally {
        setIsSearching(false);
      }
    }, DEBOUNCE_MS);

    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [query, getAccessToken]);

  const handleSelect = (result: SearchResult) => {
    setIsOpen(false);
    setQuery('');
    if (result.type === 'case') {
      navigate(`/cases/${result.id}`);
    } else {
      navigate(`/cases/${result.case_id}/evidence/${result.id}`);
    }
  };

  return (
    <div className="search-box-wrapper" style={{ position: 'relative' }}>
      <div className="search-box">
        <Search size={14} />
        <input
          type="text"
          placeholder="Search case, evidence ID…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => results.length > 0 && setIsOpen(true)}
          onBlur={() => setTimeout(() => setIsOpen(false), 150)}
          style={{
            background: 'transparent',
            border: 'none',
            outline: 'none',
            color: 'inherit',
            width: '100%',
          }}
        />
      </div>

      {isOpen && (
        <div className="search-dropdown">
          {isSearching && <div className="search-dropdown-empty">Searching…</div>}
          {!isSearching && results.length === 0 && (
            <div className="search-dropdown-empty">No matches</div>
          )}
          {!isSearching &&
            results.map((r) => (
              <div
                key={`${r.type}-${r.id}`}
                className="search-dropdown-item"
                // onMouseDown (not onClick) fires before the input's onBlur closes the dropdown
                onMouseDown={() => handleSelect(r)}
              >
                <span className="search-dropdown-label">{r.label}</span>
                <span className="search-dropdown-title">{r.title}</span>
              </div>
            ))}
        </div>
      )}
    </div>
  );
}

export default SearchBar;