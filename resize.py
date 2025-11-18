import argparse
import os
import glob
from PIL import Image


def resize_image(image_path, output_dir, size=(1280, 720)):
    """
    画像を指定されたサイズにリサイズする。
    高さをsize[1]に合わせてアスペクト比を維持してリサイズし、
    幅が不足する場合は左右に透過の余白を追加する。

    Args:
        image_path: 入力画像のパス
        output_dir: 出力ディレクトリ
        size: 目標サイズ (width, height)
    """
    # 画像を開く
    img = Image.open(image_path)

    # 元の画像サイズ
    original_width, original_height = img.size
    target_width, target_height = size

    # 高さを基準にリサイズ比率を計算
    ratio = target_height / original_height
    new_width = int(original_width * ratio)
    new_height = target_height

    # アスペクト比を維持してリサイズ
    resized_img = img.resize((new_width, new_height), Image.LANCZOS)

    # 新しい画像を作成（透過背景）
    final_img = Image.new("RGBA", size, (0, 0, 0, 0))

    # 幅が目標幅に満たない場合、中央に配置
    if new_width < target_width:
        # 左右の余白を計算
        left_padding = (target_width - new_width) // 2
        final_img.paste(resized_img, (left_padding, 0))
    else:
        # 幅が目標幅以上の場合はそのまま貼り付け
        final_img.paste(resized_img, (0, 0))

    # 出力ディレクトリが指定されていない場合は入力ディレクトリと同じ
    if output_dir is None:
        output_dir = os.path.dirname(image_path)

    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)

    # 出力ファイル名を生成
    filename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, filename)

    # 画像を保存
    final_img.save(output_path, "PNG")


def main():
    parser = argparse.ArgumentParser(
        description="Resize images to specified dimensions."
    )
    parser.add_argument("input_dir", type=str, help="Input Image Directory")
    parser.add_argument(
        "--output", "-o", type=str, default="./outdir", help="Output Directory"
    )
    parser.add_argument(
        "--width", "-w", type=int, default=1280, help="Output Image Width"
    )
    parser.add_argument(
        "--height", "-h", type=int, default=720, help="Output Image Height"
    )

    args = parser.parse_args()

    images = glob.glob(os.path.join(args.input_dir, "*.png"))
    for img_path in images:
        resize_image(img_path, args.output, size=(args.width, args.height))


if __name__ == "__main__":
    main()
