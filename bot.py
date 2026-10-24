"""OOTv2 Bot - Standard Library Only, Stateless MVP Protocol v1.
Tuân thủ luật OOTv2: Xếp tự động 9 quân và chọn nước đi hợp lệ.
"""

import json
import sys
import random

def log(message):
    """In log debug ra stderr để không làm ảnh hưởng luồng JSON trên stdout."""
    print(f"[OOTv2-Bot] {message}", file=sys.stderr, flush=True)

def handle_setup(request):
    """Xử lý xếp quân tự động (setup phase):
    Nhận danh sách 9 quân cờ (my_pieces) và các ô trống hợp lệ (available_squares).
    Phân bổ toàn bộ quân cờ vào các ô trống theo quy định của map.
    """
    pieces = request.get("my_pieces", [])
    squares = request.get("available_squares", [])
    
    if not pieces or not squares:
        raise ValueError("Thiếu dữ liệu quân cờ hoặc ô trống để xếp quân.")
    
    # Xáo trộn danh sách ô trống để tạo vị trí ngẫu nhiên hợp lệ
    target_squares = list(squares)
    random.shuffle(target_squares)
    
    placements = []
    for index, piece in enumerate(pieces):
        if index < len(target_squares):
            placements.append({
                "piece_id": piece["id"],
                "square": target_squares[index]
            })
            
    log(f"Đã tự động xếp thành công {len(placements)} quân cờ.")
    return {"placements": placements}

def handle_move(request):
    """Xử lý lượt đi (move phase):
    Nhận danh sách các nước đi hợp lệ (legal_moves).
    Ưu tiên chọn nước đi bắt quân (nếu có), hoặc chọn ngẫu nhiên một nước đi hợp lệ khác.
    """
    moves = request.get("legal_moves", [])
    if not moves:
        raise ValueError("Không còn nước đi hợp lệ nào!")
    
    # Ưu tiên các nước đi thực hiện bắt quân (capture)
    captures = [m for m in moves if m.get("is_capture") or m.get("captures") or m.get("captured")]
    if captures:
        chosen_move = random.choice(captures)
        log("Thực hiện nước đi tấn công/bắt quân.")
    else:
        chosen_move = random.choice(moves)
        log("Thực hiện nước đi di chuyển.")
        
    return chosen_move

def main():
    try:
        # Đọc request JSON từ stdin do server gửi tới
        line = sys.stdin.readline()
        if not line:
            return
        
        request = json.loads(line)

        # Kiểm tra phiên bản protocol
        if request.get("protocol_version") != 1:
            raise ValueError("Phiên bản protocol không được hỗ trợ.")

        kind = request.get("request")
        if kind == "setup":
            response = handle_setup(request)
        elif kind == "move":
            response = handle_move(request)
        else:
            raise ValueError(f"Loại yêu cầu không hợp lệ: {kind}")

        # Trả kết quả JSON về cho server qua stdout
        sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
        sys.stdout.flush()

    except Exception as error:
        log(f"Lỗi thực thi Bot: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
