# `stages.md` format

Use this exact structure. One `##` section per stage. Keep the field order
consistent so mentor mode can scan it reliably across a long curriculum.

```markdown
# <Project Name> — Build-From-Scratch Curriculum

**Target:** <one-line description of what's being built>
**Reference:** <repo URL + commit/tag pinned, OR spec/RFC name, OR "custom design doc">
**Language:** <language>
**Scope:** <weekend MVP / multi-week project / etc., and what's in vs. out of scope>

## Stage list

1. Stage 1 title
2. Stage 2 title
...

---

## Stage 1: <Title>

- **Concept(s):** <one line>
- **Difficulty:** light | medium | heavy
- **Estimated time:** <e.g. 45-60 min>
- **Why it matters:** <2-4 sentences of real-world context>
- **Reference:** `path/to/file.ext:120-168` (or spec section, or design-doc link)
- **Depends on:** Stage <N> (or "none — this is the first stage")

### Task

<Precise description of required behavior/contract. Phrased as "what,"
not "how.">

### Interface / contract

```<language>
<exact function signature(s) / struct(s) / message shape(s) the
surrounding boilerplate expects>
```

### Verification

```bash
<exact command(s) to run>
```
Expected result: <what success looks like>

### Design questions (for mentor mode to raise before coding starts)

- <question 1>
- <question 2>

### Hints (do not reveal unless asked; escalate one level at a time)

1. **Level 1:** <conceptual nudge>
2. **Level 2:** <structural/pseudocode approach>
3. **Level 3:** <near-solution guidance / illustrative snippet of an
   adjacent problem>
4. **Level 4 (last resort):** <minimal snippet that unblocks the single
   stuck point>

---

## Stage 2: <Title>
...
```

## Worked example

Below is a complete example stage from a "build your own Redis" curriculum
in Go, showing the expected level of specificity.

```markdown
## Stage 3: RESP protocol parser

- **Concept(s):** Parsing a length-prefixed, line-delimited binary protocol
- **Difficulty:** medium
- **Estimated time:** 60-90 min
- **Why it matters:** Redis clients and servers speak RESP (REdis
  Serialization Protocol) over a raw TCP stream. Every command you'll
  implement later arrives as RESP bytes, so getting the parser right — and
  right in the face of partial reads — is the load-bearing piece of the
  entire project. This is also a great worked example of the general
  "framing" problem in any binary protocol over a stream socket.
- **Reference:** `redis/src/resp_parser.c:1-140` in the real Redis source
  covers the analogous parsing logic; for this stage, follow the RESP2 spec
  at https://redis.io/docs/reference/protocol-spec/ rather than the C
  implementation's exact structure, since Go's idioms differ substantially.
- **Depends on:** Stage 2 (raw TCP echo server)

### Task

Implement a function that reads RESP-encoded "arrays of bulk strings" (the
form Redis clients use to send commands) from a stream and returns the
decoded list of strings, correctly handling the case where a single TCP
read doesn't contain a full message yet.

### Interface / contract

```go
// ParseCommand reads one full RESP command (an array of bulk strings)
// from r. It returns the decoded arguments, or an error if the stream
// is malformed. It must block/retry internally until a full command is
// available — callers should not need to pre-buffer.
func ParseCommand(r *bufio.Reader) ([]string, error)
```

### Verification

```bash
go test ./resp/... -run TestParseCommand -v
```
Expected result: all table-driven test cases in `resp/parser_test.go`
pass, including the "split across two reads" and "empty array" cases.

### Design questions (for mentor mode to raise before coding starts)

- RESP gives you the length of each bulk string up front. Do you read
  exactly that many bytes, or read-until-delimiter like the array count
  line? Why does RESP bother giving lengths for one part and not the
  other?
- What should happen if the declared length is absurd (e.g. larger than
  any real command could be)? Is that this stage's problem to solve or a
  later "hardening" stage's?

### Hints

1. **Level 1:** `bufio.Reader` gives you `ReadString(byte)` for
   delimiter-based reads and `io.ReadFull` for exact-length reads — RESP
   needs both, in different places. Which parts of the format are
   delimited and which are length-prefixed?
2. **Level 2:** Read the `*<count>\r\n` line to find out how many elements
   are coming. For each element, read the `$<length>\r\n` line, then
   `io.ReadFull` exactly `length` bytes plus the trailing `\r\n`. Repeat
   `count` times.
3. **Level 3:** Watch the trailing `\r\n` after each bulk string's payload
   — it's easy to read `length` bytes and forget to also consume the two
   delimiter bytes after it, which desyncs every subsequent read on the
   same connection.
4. **Level 4 (last resort):**
   ```go
   n, err := io.ReadFull(r, buf[:length])
   if err != nil { return nil, err }
   r.Discard(2) // consume trailing \r\n
   ```
```

## Notes on citing reference source

- Cite exact file + line ranges you've actually read, never guessed ranges.
- Never reproduce large chunks of the reference source into `stages.md` —
  point at it, don't paste it. A short (under ~15 word) illustrative
  fragment is fine if truly necessary; anything longer, just describe it in
  your own words and give the pointer.
- If the reference project has since changed, pin the commit hash or tag
  you read so line numbers stay valid for the user.
