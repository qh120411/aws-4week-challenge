# Phần 1: Lý thuyết Tuần 1

## 1. Lý thuyết cơ bản

### Tài liệu

[Lý thuyết mạng cơ bản – ghi chú bởi qhuy](https://app.notion.com/p/I-M-ng-c-b-n-3e4c95e87f8d80ffb1cfe05288b4c082?source=copy_link)

## 2. Sơ đồ kiến trúc VPC

``` mermaid
flowchart TB
    Internet["Internet"] <--> IGW["Internet Gateway"]

    subgraph VPC["Amazon VPC: 10.0.0.0/16"]
        direction TB

        subgraph AZ1["Availability Zone 1"]
            direction LR
            PUB1["Public Subnet 1 (10.0.1.0/24)"]
            NAT1["NAT Gateway 1"]
            PRI1["Private Subnet 1 (10.0.2.0/24)"]

            PUB1 --- NAT1
            PRI1 -->|"Private Route Table"| NAT1
        end

        subgraph AZ2["Availability Zone 2"]
            direction LR
            PUB2["Public Subnet 2 (10.0.3.0/24)"]
            NAT2["NAT Gateway 2"]
            PRI2["Private Subnet 2 (10.0.4.0/24)"]

            PUB2 --- NAT2
            PRI2 -->|"Private Route Table"| NAT2
        end
    end

    IGW <-->|"Public Route Table"| PUB1
    IGW <-->|"Public Route Table"| PUB2
```

Public Subnet sử dụng Route Table có tuyến mặc định trỏ đến Internet Gateway:

```text
0.0.0.0/0 → Internet Gateway
```

Private Subnet không có đường đi trực tiếp đến Internet Gateway. Khi tài nguyên trong Private Subnet cần chủ động truy cập Internet, traffic được chuyển qua NAT Gateway:

```text
Private Subnet
→ NAT Gateway
→ Internet Gateway
→ Internet
```

Hai Availability Zone giúp hạ tầng sẵn sàng mở rộng theo hướng High Availability. Khi triển khai trong môi trường production, mỗi AZ có thể chứa một máy chủ ứng dụng để hệ thống tiếp tục hoạt động nếu một AZ gặp sự cố.

> Trong phạm vi challenge, có thể sử dụng một NAT Gateway để tiết kiệm chi phí. Kiến trúc production nên đặt một NAT Gateway trong mỗi Availability Zone.

## 3. Giải thích nguyên lý cô lập mạng

### Tại sao Database và Application Server nên được đặt trong Private Subnet?

Database và Application Server thường chứa dữ liệu hoặc xử lý các nghiệp vụ quan trọng. Đặt các tài nguyên này trong Private Subnet giúp ngăn truy cập trực tiếp từ Internet, giảm bề mặt tấn công và tăng khả năng bảo vệ hệ thống.

Người dùng chỉ truy cập vào thành phần công khai như Application Load Balancer. Load Balancer sau đó chuyển request đến Application Server thông qua mạng nội bộ của VPC.

```text
Internet
→ Application Load Balancer trong Public Subnet
→ Application Server trong Private Subnet
→ Database trong Private Subnet
```

### So sánh Security Group và Network ACL

| Tiêu chí | Security Group | Network ACL |
|---|---|---|
| Phạm vi bảo vệ | Gắn với tài nguyên hoặc network interface | Gắn với toàn bộ subnet |
| Cơ chế | Stateful | Stateless |
| Loại rule | Chỉ có `ALLOW` | Có cả `ALLOW` và `DENY` |
| Cách xét rule | Tổng hợp tất cả các rule | Xét theo thứ tự rule number |
| Traffic phản hồi | Tự động cho phép phản hồi của kết nối hợp lệ | Phải cấu hình rule cho cả hai chiều |
