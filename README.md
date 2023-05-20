<!-- Folder structure -->
# Python + Flask + MySQL + Docker

<p align="center">
  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg" alt="Python Logo" width="50" height="50"/>
  <img src="https://github.com/devicons/devicon/blob/master/icons/flask/flask-original-wordmark.svg" alt="Flask Logo" width="50" height="50"/>
  <img src="https://github.com/devicons/devicon/blob/master/icons/mysql/mysql-original-wordmark.svg" alt="MySQL Logo" width="50" height="50"/>
  <img src="https://github.com/devicons/devicon/blob/master/icons/docker/docker-plain.svg" alt="Docker Logo" width="50" height="50"/>
</p>

## Description
Timetable-Generator-GA made with ❤️ by [L-3012](https://github.com/lov3five).

## Start Guide

### Hướng dẫn sử dụng requirements.txt
- requirements.txt là một file chứa danh sách các package Python cần thiết cho một ứng dụng hoặc một dự án. Bằng cách sử dụng pip, một công cụ quản lý package Python, chúng ta có thể cài đặt tất cả các package được liệt kê trong requirements.txt chỉ bằng một lệnh đơn giản.

- Để cài đặt các package được liệt kê trong requirements.txt, hãy làm theo các bước sau:

    - Mở terminal/command prompt và di chuyển đến thư mục chứa requirements.txt.

    - Tạo một virtual environment (venv) để cài đặt các package vào venv đó. Điều này giúp tránh xung đột giữa các package khác nhau trong các dự án khác nhau. Hãy đọc phần sau để biết cách tạo và sử dụng một venv.

    - Cài đặt `pip` nếu nó chưa được cài đặt bằng cách chạy lệnh sau:
    ```
    python3 -m ensurepip --default-pip
    ```

    - Cài đặt các package từ requirements.txt bằng lệnh sau:
    ```
    pip install -r requirements.txt
    ```
    > Lệnh này sẽ cài đặt tất cả các package được liệt kê trong requirements.txt vào venv đang được sử dụng.

### Hướng dẫn sử dụng virtual environment (venv)
- Virtual environment (venv) là một công cụ giúp cài đặt và quản lý các package Python trên một môi trường độc lập, tách biệt với các package Python cài đặt trên hệ thống mà không phụ thuộc vào chúng. Venv giúp cho việc phát triển các dự án Python dễ dàng và đảm bảo tính đồng nhất của môi trường phát triển và triển khai.

- Để tạo một venv mới, hãy làm theo các bước sau:

    - Mở terminal/command prompt và di chuyển đến thư mục của dự án.

    - Tạo một venv bằng lệnh sau:
    ```
    python3 -m venv venv
    ```
    > Lệnh này sẽ tạo một thư mục venv chứa môi trường độc lập cho dự án của bạn. Nếu bạn đặt tên khác cho thư mục venv, hãy thay thế venv bằng tên thư mục của bạn trong các lệnh tiếp theo.
    - Kích hoạt venv bằng lệnh sau:
    
    `Windows`
    ```
    venv\Scripts\activate.bat
    ```
    > Lệnh này sẽ kích hoạt venv, tạo ra một môi trường độc lập để cài đặt và quản lý các package.

    - Để thoát khỏi venv (quay lại môi trường `global` của Python), hãy sử dụng lệnh sau:
    ```
    deactivate
    ```
### Hướng dẫn chạy docker-compose.yml
>>> 🔴  Chú ý: Để sử dụng docker-compose, chúng ta cần cài đặt Docker và docker-compose trên máy tính của mình. Hãy truy cập trang chủ của Docker để tải và cài đặt phiên bản phù hợp với hệ điều hành của bạn.
- docker-compose.yml là một file định nghĩa các service và các container được sử dụng trong một ứng dụng Docker. Bằng cách sử dụng docker-compose, một công cụ quản lý container Docker, chúng ta có thể chạy một ứng dụng với nhiều container khác nhau chỉ bằng một lệnh đơn giản.

- Để chạy một ứng dụng với các container được định nghĩa trong docker-compose.yml, hãy làm theo các bước sau:

    - Mở Command Prompt và di chuyển đến thư mục chứa docker-compose.yml bằng lệnh cd. Ví dụ:
    ```
    cd C:\path\to\project
    ```
    - Sử dụng lệnh sau để chạy ứng dụng với các container được định nghĩa trong docker-compose.yml:
    ```
    docker-compose up
    ```
    > Lệnh này sẽ tải các image cần thiết và khởi động các container. Nếu docker-compose.yml được cập nhật, chúng ta có thể sử dụng lệnh này để cập nhật lại các container.
    
    - ❗❗❗ Để dừng các container, hãy sử dụng lệnh sau ❗❗❗:
    ```
    docker-compose down
    ```
    > Lệnh này sẽ dừng các container và xóa chúng.