Malformed timestamps

Some attempt events contained invalid ISO timestamps (e.g., invalid month values). These events were skipped during ingestion to prevent corrupt data from entering the system. The original payload is preserved when valid.