# Crawler Specifications - HK CSIP

## Target
-   **URL**: `https://www.cybersecurity.hk`
-   **Sections**:
    1.  **Advisories**: `https://www.cybersecurity.hk/en/advisories.php`
    2.  **Expert Corner**: `https://www.cybersecurity.hk/en/expert.php`

## Selectors
-   **Links**: `a[href*=".php"]`
-   **Title**: `h1.page-title::text`
-   **Content**: `div.content-area p::text, div.content-area li::text`
-   **Date**: `span.date::text`

## Logic
1.  Start at index pages.
2.  Follow pagination (if any) and article links.
3.  Extract text.
4.  Clean whitespace.
5.  Yield `HKItem`.
