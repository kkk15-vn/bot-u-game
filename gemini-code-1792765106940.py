"""OOTv2 Bot - Standard Library Only, Stateless, MVP Protocol v1."""

import json
import sys


def handle_setup(request):
    """Xử lý yêu cầu xếp quân ban đầu (setup phase)."""
    pieces = request.get("my_pieces", [])
    squares = request.get("available_squares", [])
    
    placements = []
    for index, piece in enumerate(pieces):
        if index < len(squares):
            placements.append({
                "piece_id": piece["id"],
                "square": squares[index]
            })
    return {"placements": placements}


def handle_move(request):
    """Xử lý yêu cầu chọn nước đi trong trận đấu (move phase)."""
    moves = request.get("legal_moves", [])
    if not moves:
        raise ValueError("No legal moves available")
    
    # Chiến thuật cơ bản: chọn nước đi hợp lệ đầu tiên trong danh sách
    # Bạn có thể thay đổi logic chọn nước đi thông minh hơn ở đây nếu muốn.
    return moves[0]


def main():
    try:
        # Đọc dữ liệu JSON từ stdin do server gửi sang
        line = sys.stdin.readline()
        if not line:
            return
        
        request = json.loads(line)

        # Kiểm tra version của protocol
        if request.get("protocol_version") != 1:
            raise ValueError("Unsupported protocol version")

        kind = request.get("request")
        if kind == "setup":
            response = handle_setup(request)
        elif kind == "move":
            response = handle_move(request)
        else:
            raise ValueError(f"Unknown request type: {kind}")

        # Trả kết quả dạng JSON qua stdout
        sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    except Exception as error:
        # In lỗi ra stderr (không ảnh hưởng đến luồng stdout trả về cho server)
        print(f"Bot error: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()