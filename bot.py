"""OOTv2 Bot Chuẩn - Standard Library Only, Stateless MVP Protocol v1.
"""

import json
import sys
import random

def on_setup(request):
    pieces = request["my_pieces"]
    squares = request["available_squares"]
    if len(pieces) != 9 or len(squares) < 9:
        raise ValueError("Unexpected setup request")
    
    # Xếp ngẫu nhiên 9 quân vào 9 ô available_squares đầu tiên
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
        raise ValueError("No legal moves available")
    
    # Chọn ngẫu nhiên một nước đi hợp lệ
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
