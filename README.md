# coder-kit

Bộ **skills + agents** cho Claude, phục vụ code review và các vai trò **MLE**, **Data Engineer**, **Tester**. Dùng được trên mọi app của Claude.

## Có gì bên trong

| Thành phần | Tên | Dùng ở đâu |
|---|---|---|
| Skill | `code-review` | Mọi app |
| Skill | `ml-engineering` | Mọi app |
| Skill | `data-engineering` | Mọi app |
| Skill | `test-engineering` | Mọi app |
| Subagent | `code-reviewer`, `ml-engineer`, `data-engineer`, `test-engineer` | Claude Code (CLI, IDE, Desktop Code tab), Agent SDK |
| Slash command | `/review`, `/test-plan` | Claude Code |

Skills là phần "chạy ở mọi nơi". Subagents và slash commands chỉ có trong Claude Code; ở web, Desktop chat và Chrome, chỉ cần nói "review đoạn code này" hoặc "viết test plan cho…" là skill tương ứng tự kích hoạt.

## Cài đặt

### 1. Claude Code (CLI / IDE / Desktop)
```
/plugin marketplace add quanhn9792/coder-kit
/plugin install coder-kit@coder-kit
```
Cập nhật sau này: `/plugin marketplace update coder-kit`.

### 2. claude.ai web, Claude Desktop, mobile, Claude in Chrome
Skills đồng bộ theo tài khoản, nên chỉ cần upload một lần:
1. Tải các file `*.zip` ở mục **Releases** của repo (hoặc chạy `bash scripts/build-zips.sh` để tạo trong `dist/`).
2. Vào **Settings → Capabilities → Skills** (bật *Code execution* nếu được hỏi), bấm **Upload skill**, chọn từng file zip.
3. Bật các skill vừa upload. Từ đó Desktop, mobile và Claude in Chrome (phiên Cowork) dùng chung.

### 3. Claude API / Agent SDK
Upload thư mục skill qua Skills API (`/v1/skills`), hoặc trỏ Agent SDK tới thư mục `plugins/coder-kit`.

## Cấu trúc repo
```
.claude-plugin/marketplace.json      # danh mục plugin (marketplace)
plugins/coder-kit/
  .claude-plugin/plugin.json
  skills/<skill>/SKILL.md            # hướng dẫn chính, < 500 dòng
  skills/<skill>/references/*.md     # tài liệu phụ, chỉ đọc khi cần
  agents/*.md                        # subagents cho Claude Code
  commands/*.md                      # slash commands
scripts/validate.py                  # kiểm tra định dạng
scripts/build-zips.sh                # đóng gói zip để upload
.github/workflows/release.yml        # CI: validate + build zip, tạo release khi push tag v*
```

## Thêm skill mới
1. Tạo `plugins/coder-kit/skills/<ten-skill>/SKILL.md` với frontmatter `name` (trùng tên thư mục, a-z0-9-) và `description` (nói rõ *làm gì* và *khi nào dùng*).
2. Chạy `python3 scripts/validate.py`.
3. Tăng `version` trong `plugin.json` và `marketplace.json`, push tag `vX.Y.Z` để có zip mới trong Releases.
