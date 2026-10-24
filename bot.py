"""OOTv2 Bot nâng cấp dựa trên bot mẫu MVP — Python 3.12+, chỉ standard library.

Protocol: đọc đúng 1 JSON line từ stdin và in đúng 1 JSON line ra stdout.
Bot stateless. Không in log ra stdout. 
Cải tiến: Xếp quân linh hoạt và có ưu tiên bắt quân đối phương khi có cơ hội.
"""

import json
import sys
import random


def on_setup(request):
    pieces = request["my_pieces"]
    squares = request["available_squares"]
    if len(pieces) != 9 or len(squares) < 9:
        raise ValueError("Unexpected setup request")
    
    # Cải tiến: Xáo trộn nhẹ các ô available_squares để thế trận xếp quân không bị trùng lặp
    target_squares = list(squares[:9])
    random.shuffle(target_squares)
    
    return {
        "placements": [
            {"piece_id": piece["id"], "square": square}
            for piece, square in zip(pieces, target_squares)
        ]
    }


def on_move(request):
    legal_moves = request["legal_moves"]
    if not legal_moves:
        # Judge phải xử lý no_legal_move trước khi gọi bot.
        raise ValueError("No legal moves available")
    
    # Cải tiến chiến thuật: Ưu tiên chọn nước đi ăn quân đối phương (nếu có)
    captures = [m for m in legal_moves if m.get("is_capture") or m.get("captures")]
    if captures:
        return random.choice(captures)
    
    # Nếu không có nước ăn quân, chọn ngẫu nhiên một nước đi hợp lệ để tăng tính biến hóa
    return random.choice(legal_moves)


def main():
    line = sys.stdin.readline()
    if not line:
        raise ValueError("No input provided")
    request = json.loads(line)
    if request.get("protocol_version") != 1:
        raise ValueError("Unsupported protocol version")

    request_type = request.get("request")
    if request_type == "setup":
        response = on_setup(request)
    elif request_type == "move":
        response = on_move(request)
    else:
        raise ValueError(f"Unsupported request: {request_type}")

    sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"Bot failed: {error}", file=sys.stderr)
        sys.exit(1)
