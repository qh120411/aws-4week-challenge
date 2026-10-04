# Phần 1: Lý thuyết Tuần 2

## 1. Packet Walk

### Inbound Traffic

Luồng traffic từ Internet vào ứng dụng:

```text
Internet
   ↓
Internet Gateway (IGW)
   ↓
Application Load Balancer (Public Subnet)
   ↓
App Server / FastAPI (Private Subnet)
   ↓
Database (nếu có)
```

- **IGW** giúp VPC giao tiếp với Internet.
- **ALB** nhận request từ người dùng và chuyển tiếp vào App Server.
- **App Server** đặt trong Private Subnet để tránh bị truy cập trực tiếp từ Internet.
- Nếu có Database, chỉ App Server được phép kết nối tới Database.

Ví dụ:

```text
Client → HTTPS :443 → ALB → FastAPI :8000
```

---

### Outbound Traffic

Khi App Server trong Private Subnet cần truy cập Internet:

```text
App Server
   ↓
NAT Gateway (Public Subnet)
   ↓
Internet Gateway
   ↓
Internet
```

Ví dụ:

- `pip install`
- `apt update`
- `docker pull`
- tải model AI
- gọi API bên ngoài

Private EC2 không cần Public IP. NAT Gateway sẽ đại diện cho EC2 truy cập Internet.

Private Route Table:

```text
10.0.0.0/16 → local
0.0.0.0/0   → NAT Gateway
```

Public Route Table:

```text
10.0.0.0/16 → local
0.0.0.0/0   → Internet Gateway
```

---

## 2. Security Group

Security Group là firewall của AWS, kiểm soát traffic **Inbound** và **Outbound**.

Security Group hoạt động theo cơ chế **Stateful**: nếu request được phép đi vào thì response tương ứng được phép đi ra.

### ALB Security Group

| Direction | Port | Source / Destination | Mục đích |
|---|---:|---|---|
| Inbound | 80 | `0.0.0.0/0` | HTTP |
| Inbound | 443 | `0.0.0.0/0` | HTTPS |
| Outbound | 8000 | `sg-app` | Gửi request tới FastAPI |

---

### App Server Security Group

| Direction | Port | Source / Destination | Mục đích |
|---|---:|---|---|
| Inbound | 8000 | `sg-alb` | Chỉ nhận request từ ALB |
| Outbound | 80/443 | `0.0.0.0/0` | Update, tải package, gọi API |
| Outbound | 5432 / 3306 | `sg-db` | Kết nối Database nếu có |

Không nên mở:

```text
Port 8000 → 0.0.0.0/0
```

Nên dùng:

```text
Port 8000 → Source: sg-alb
```

---

### Database Security Group

Nếu dùng PostgreSQL:

```text
Port: 5432
Source: sg-app
```

Nếu dùng MySQL:

```text
Port: 3306
Source: sg-app
```

Database không nên cho phép:

```text
0.0.0.0/0
```

---

## 3. Áp dụng cho Banking Intent API

Hiện tại project chưa dùng Database nên kiến trúc có thể là:

```text
Internet
   ↓
IGW
   ↓
ALB
   ↓
FastAPI EC2 (Private Subnet)
```

Outbound:

```text
FastAPI EC2
   ↓
NAT Gateway
   ↓
IGW
   ↓
Internet
```

Nguyên tắc chính:

```text
Internet → ALB → App
App → NAT → Internet
```

App Server không cần Public IP và chỉ nhận traffic từ ALB.
