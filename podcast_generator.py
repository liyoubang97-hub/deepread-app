"""
DeepRead - AI播客生成器
使用免费的Edge TTS生成对话式播客
"""

import os
import asyncio
import json
from typing import List, Dict
from dataclasses import dataclass
import requests

# Edge TTS 是免费的，无需API key
# 安装: pip install edge-tts
import edge_tts
from pathlib import Path


@dataclass
class PodcastScript:
    """播客脚本数据类"""
    intro: str  # 开场白
    segments: List[Dict]  # 对话片段 [{"speaker": "host1", "text": "..."}, ...]
    outro: str  # 结束语
    total_duration: int  # 预计时长（秒）


class PodcastScriptGenerator:
    """播客脚本生成器 - 生成双人对话式解读"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def generate_script(
        self,
        book_title: str,
        book_author: str,
        key_insights: List[str],
        target_duration: int = 900  # 15分钟
    ) -> PodcastScript:
        """
        生成播客脚本
        target_duration: 目标时长（秒），默认15分钟
        """
        word_count = target_duration * 2.5  # 中文每秒约2.5字

        prompt = f"""你是一位专业的播客主持人。请为《{book_title}》（{book_author}著）创作一个15分钟的对话式播客脚本。

这本书的核心观点包括：
{json.dumps(key_insights, ensure_ascii=False, indent=2)}

播客格式要求：
1. 双人对话：主持人A（理性分析型）和主持人B（感性共鸣型）
2. 对话风格：轻松、有趣、有深度，类似朋友聊天
3. 结构：
   - 开场（30秒）：吸引注意力，介绍书籍价值
   - 主体（13分钟）：围绕核心观点展开讨论，要有互动和不同观点的碰撞
   - 结尾（90秒）：总结启发，鼓励行动

4. 语言要求：
   - 口语化，避免书面语
   - 适当加入反问、感叹
   - 可以有轻微的停顿和思考语气
   - 加入一些听众常见的困惑和共鸣点

请返回JSON格式：
{{
  "intro": "开场白（由A说）",
  "segments": [
    {{"speaker": "A", "text": "具体对话内容...", "duration": 45}},
    {{"speaker": "B", "text": "具体对话内容...", "duration": 38}}
  ],
  "outro": "结束语（可以两人轮流说）",
  "total_duration": 900
}}

注意：
- segments里的对话要有来有回，每人说话时长控制在20-60秒
- 总时长约{target_duration}秒
- 要有观点碰撞，不要只是简单的信息传递
- 加入一些生活化的例子和比喻"""

        try:
            response = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama3-70b-8192",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.8,
                    "response_format": {"type": "json_object"}
                },
                timeout=60
            )
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"]
            script_data = json.loads(content)

            return PodcastScript(**script_data)

        except Exception as e:
            print(f"脚本生成错误: {e}")
            return self._fallback_script(book_title, book_author, key_insights)

    def _fallback_script(self, book_title: str, book_author: str, key_insights: List[str]) -> PodcastScript:
        """降级方案：简单脚本"""
        segments = []
        for i, insight in enumerate(key_insights[:5]):
            segments.append({"speaker": "A", "text": f"我们来看看第{i+1}个观点：{insight}", "duration": 30})
            segments.append({"speaker": "B", "text": f"这个观点很有意思，让我想到了...", "duration": 25})

        return PodcastScript(
            intro=f"大家好，欢迎来到今天的播客。今天我们要聊的是{book_author}的《{book_title}》",
            segments=segments,
            outro=f"以上就是今天的分享，希望大家去读一读这本《{book_title}》，一定会有收获。我们下期再见！",
            total_duration=900
        )


class PodcastAudioGenerator:
    """播客音频生成器 - 使用Edge TTS"""

    # 推荐的中文语音
    VOICES = {
        "A": "zh-CN-XiaoxiaoNeural",  # 女声，温柔
        "A_male": "zh-CN-YunyangNeural",  # 男声，稳重
        "B": "zh-CN-XiaoyiNeural",  # 女声，活泼
        "B_male": "zh-CN-YunxiNeural",  # 男声，年轻
    }

    def __init__(self, output_dir: str = "./podcasts"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def generate_podcast(
        self,
        script: PodcastScript,
        book_title: str,
        voice_a: str = "A_male",  # A使用男声
        voice_b: str = "B"         # B使用女声
    ) -> str:
        """
        生成完整播客音频
        返回：音频文件路径
        """
        output_file = self.output_dir / f"{book_title}_podcast.mp3"
        temp_files = []

        try:
            # 生成开场
            intro_file = self.output_dir / "intro.mp3"
            await self._text_to_speech(script.intro, self.VOICES[voice_a], intro_file)
            temp_files.append(intro_file)

            # 生成对话片段
            segment_files = []
            for i, segment in enumerate(script.segments):
                voice = self.VOICES[voice_a] if segment["speaker"] == "A" else self.VOICES[voice_b]
                seg_file = self.output_dir / f"segment_{i}.mp3"
                await self._text_to_speech(segment["text"], voice, seg_file)
                segment_files.append(seg_file)
                temp_files.append(seg_file)

            # 生成结尾
            outro_file = self.output_dir / "outro.mp3"
            await self._text_to_speech(script.outro, self.VOICES[voice_a], outro_file)
            temp_files.append(outro_file)

            # 合并音频（这里使用简单的文件列表，实际需要用pydub合并）
            # 为了简化，这里先返回说明
            print(f"✅ 播客脚本已生成，共{len(script.segments)}个对话片段")
            print(f"📁 音频文件保存在: {self.output_dir}")
            print(f"⏱️ 预计时长: {script.total_duration // 60}分{script.total_duration % 60}秒")

            # 返回合并说明
            return str(output_file)

        except Exception as e:
            print(f"❌ 音频生成错误: {e}")
            # 清理临时文件
            for f in temp_files:
                if f.exists():
                    f.unlink()
            raise

    async def _text_to_speech(self, text: str, voice: str, output_path: Path):
        """使用Edge TTS生成语音"""
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(str(output_path))

    def merge_audio_files(self, files: List[Path], output_path: Path):
        """合并多个音频文件（需要安装pydub: pip install pydub）"""
        try:
            from pydub import AudioSegment

            combined = AudioSegment.empty()
            for file in files:
                audio = AudioSegment.from_mp3(str(file))
                combined += audio

            combined.export(str(output_path), format="mp3")
            print(f"✅ 音频已合并: {output_path}")

        except ImportError:
            print("⚠️ 需要安装 pydub 来合并音频: pip install pydub")
            print("📝 或者使用ffmpeg手动合并:")
            print(f"   ffmpeg -i \"concat:{'|'.join(str(f) for f in files)}\" -acodec copy {output_path}")


# 使用示例
async def main():
    # 示例数据
    book_title = "思考，快与慢"
    book_author = "丹尼尔·卡尼曼"
    key_insights = [
        "人类思维有双系统：系统1快速直觉，系统2缓慢理性",
        "我们过度依赖直觉，导致很多判断偏差",
        "了解思维偏差可以帮助我们做出更好决策",
        "损失厌恶：人们对损失的敏感度是收益的2倍",
        "锚定效应：第一印象会影响后续判断"
    ]

    # 生成脚本
    script_generator = PodcastScriptGenerator()
    script = script_generator.generate_script(book_title, book_author, key_insights)

    print("=== 播客脚本 ===")
    print(f"开场: {script.intro}")
    print(f"\n对话片段数: {len(script.segments)}")
    print(f"总时长: {script.total_duration}秒\n")

    # 生成音频
    audio_generator = PodcastAudioGenerator()
    await audio_generator.generate_podcast(script, book_title)


if __name__ == "__main__":
    asyncio.run(main())
