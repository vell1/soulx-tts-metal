#!/usr/bin/env python3
"""
SoulX-Podcast TTS 性能监控工具

实时监控 TTS 服务的性能指标，包括：
- 各阶段耗时
- 实时因子 (RTF)
- 系统资源使用
"""

import re
import sys
import time
import subprocess
from datetime import datetime
from collections import deque

# ANSI 颜色代码
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class PerformanceMonitor:
    def __init__(self, log_file="/tmp/soulx_optimized.log"):
        self.log_file = log_file
        self.stats = {
            "total_requests": 0,
            "parse_times": deque(maxlen=10),
            "preprocess_times": deque(maxlen=10),
            "inference_times": deque(maxlen=10),
            "postprocess_times": deque(maxlen=10),
            "total_times": deque(maxlen=10),
            "rtf_values": deque(maxlen=10),
            "audio_durations": deque(maxlen=10),
        }
    
    def clear_screen(self):
        """清屏"""
        print("\033[2J\033[H", end="")
    
    def print_header(self):
        """打印标题"""
        print(f"{Colors.BOLD}{Colors.CYAN}=" * 80)
        print(f"{'🎙️  SoulX-Podcast TTS 性能监控':^80}")
        print(f"{'=' * 80}{Colors.END}\n")
        print(f"监控时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"日志文件: {self.log_file}")
        print(f"累计请求: {self.stats['total_requests']}\n")
    
    def print_current_stats(self):
        """打印当前统计"""
        if not self.stats['total_times']:
            print(f"{Colors.YELLOW}等待数据...{Colors.END}")
            return
        
        # 计算平均值
        avg_parse = sum(self.stats['parse_times']) / len(self.stats['parse_times'])
        avg_preprocess = sum(self.stats['preprocess_times']) / len(self.stats['preprocess_times'])
        avg_inference = sum(self.stats['inference_times']) / len(self.stats['inference_times'])
        avg_postprocess = sum(self.stats['postprocess_times']) / len(self.stats['postprocess_times'])
        avg_total = sum(self.stats['total_times']) / len(self.stats['total_times'])
        avg_rtf = sum(self.stats['rtf_values']) / len(self.stats['rtf_values'])
        avg_audio = sum(self.stats['audio_durations']) / len(self.stats['audio_durations'])
        
        # 最新值
        latest_parse = self.stats['parse_times'][-1]
        latest_preprocess = self.stats['preprocess_times'][-1]
        latest_inference = self.stats['inference_times'][-1]
        latest_postprocess = self.stats['postprocess_times'][-1]
        latest_total = self.stats['total_times'][-1]
        latest_rtf = self.stats['rtf_values'][-1]
        latest_audio = self.stats['audio_durations'][-1]
        
        # 打印表格
        print(f"{Colors.BOLD}📊 性能指标（最近 10 次请求）{Colors.END}")
        print(f"\n{'阶段':<25} {'最新值':<15} {'平均值':<15} {'占比':<10}")
        print("-" * 70)
        
        # 各阶段
        self._print_row("1️⃣  输入解析", latest_parse, avg_parse, avg_parse/avg_total*100)
        self._print_row("2️⃣  数据预处理 [CPU]", latest_preprocess, avg_preprocess, avg_preprocess/avg_total*100, Colors.YELLOW)
        self._print_row("3️⃣  模型推理 [GPU]", latest_inference, avg_inference, avg_inference/avg_total*100, Colors.CYAN)
        self._print_row("4️⃣  后处理", latest_postprocess, avg_postprocess, avg_postprocess/avg_total*100)
        print("-" * 70)
        self._print_row(f"{Colors.BOLD}总计{Colors.END}", latest_total, avg_total, 100, Colors.GREEN)
        
        print(f"\n{Colors.BOLD}🎵 音频统计{Colors.END}")
        print(f"  最新音频时长: {latest_audio:.2f}s")
        print(f"  平均音频时长: {avg_audio:.2f}s")
        
        print(f"\n{Colors.BOLD}⚡ 实时因子 (RTF){Colors.END}")
        rtf_color = Colors.GREEN if avg_rtf < 1.0 else Colors.YELLOW if avg_rtf < 3.0 else Colors.RED
        print(f"  最新 RTF: {rtf_color}{latest_rtf:.2f}x{Colors.END} (耗时 / 音频时长)")
        print(f"  平均 RTF: {rtf_color}{avg_rtf:.2f}x{Colors.END}")
        print(f"  {'✅ 实时性能优秀' if avg_rtf < 1.0 else '⚠️  非实时处理'}")
        
        # 性能分析
        print(f"\n{Colors.BOLD}💡 性能分析{Colors.END}")
        bottleneck = max([
            ("数据预处理", avg_preprocess),
            ("模型推理", avg_inference),
        ], key=lambda x: x[1])
        print(f"  瓶颈阶段: {bottleneck[0]} ({bottleneck[1]:.2f}s, {bottleneck[1]/avg_total*100:.1f}%)")
        
        if avg_preprocess / avg_total > 0.1:
            print(f"  {Colors.YELLOW}💡 建议: 数据预处理占比较高，可考虑缓存优化{Colors.END}")
        if avg_rtf > 3.0:
            print(f"  {Colors.YELLOW}💡 建议: RTF较高，考虑使用更强GPU或减少推理步数{Colors.END}")
    
    def _print_row(self, name, latest, avg, percentage, color=""):
        """打印表格行"""
        bar_length = int(percentage / 2)
        bar = "█" * bar_length
        print(f"{name:<25} {color}{latest:>6.3f}s{Colors.END}      {color}{avg:>6.3f}s{Colors.END}      {bar} {percentage:>5.1f}%")
    
    def parse_log_line(self, line):
        """解析日志行"""
        # 解析各阶段耗时
        if "[PERF] 输入解析:" in line:
            match = re.search(r'(\d+\.\d+)s', line)
            if match:
                self.stats['parse_times'].append(float(match.group(1)))
        
        elif "[PERF] 数据预处理" in line:
            match = re.search(r'(\d+\.\d+)s', line)
            if match:
                self.stats['preprocess_times'].append(float(match.group(1)))
        
        elif "[PERF] 模型推理" in line:
            match = re.search(r'(\d+\.\d+)s', line)
            if match:
                self.stats['inference_times'].append(float(match.group(1)))
        
        elif "[PERF] 后处理:" in line:
            match = re.search(r'(\d+\.\d+)s', line)
            if match:
                self.stats['postprocess_times'].append(float(match.group(1)))
        
        elif "生成完成！音频:" in line:
            # 解析: 音频: 2.48s | 耗时: 8.73s | RTF: 3.52x
            match = re.search(r'音频: (\d+\.\d+)s.*耗时: (\d+\.\d+)s.*RTF: (\d+\.\d+)x', line)
            if match:
                audio_duration = float(match.group(1))
                total_time = float(match.group(2))
                rtf = float(match.group(3))
                
                self.stats['audio_durations'].append(audio_duration)
                self.stats['total_times'].append(total_time)
                self.stats['rtf_values'].append(rtf)
                self.stats['total_requests'] += 1
                
                # 刷新显示
                self.refresh_display()
    
    def refresh_display(self):
        """刷新显示"""
        self.clear_screen()
        self.print_header()
        self.print_current_stats()
        print(f"\n{Colors.BOLD}按 Ctrl+C 退出监控{Colors.END}")
    
    def watch_log(self):
        """监控日志文件"""
        print(f"{Colors.GREEN}启动监控...{Colors.END}\n")
        
        try:
            # 使用 tail -f 监控日志
            process = subprocess.Popen(
                ['tail', '-f', self.log_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            self.refresh_display()
            
            for line in process.stdout:
                self.parse_log_line(line)
        
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}监控已停止{Colors.END}")
            process.terminate()
        
        except FileNotFoundError:
            print(f"{Colors.RED}错误: 日志文件不存在: {self.log_file}{Colors.END}")
            print(f"请先启动 TTS 服务: python app.py")
            sys.exit(1)
    
    def show_system_resources(self):
        """显示系统资源使用"""
        try:
            # CPU 使用率
            cpu_output = subprocess.check_output(
                "top -l 1 | grep 'CPU usage'",
                shell=True,
                universal_newlines=True
            )
            print(f"\n{Colors.BOLD}💻 系统资源{Colors.END}")
            print(f"  {cpu_output.strip()}")
            
            # GPU 使用（如果有）
            try:
                gpu_output = subprocess.check_output(
                    "nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits",
                    shell=True,
                    universal_newlines=True,
                    stderr=subprocess.DEVNULL
                )
                gpu_util, mem_used, mem_total = gpu_output.strip().split(', ')
                print(f"  GPU 使用率: {gpu_util}%")
                print(f"  GPU 内存: {mem_used}MB / {mem_total}MB")
            except:
                pass  # 没有 NVIDIA GPU
        
        except Exception as e:
            pass


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SoulX-Podcast TTS 性能监控")
    parser.add_argument(
        "--log",
        default="/tmp/soulx_optimized.log",
        help="日志文件路径 (默认: /tmp/soulx_optimized.log)"
    )
    
    args = parser.parse_args()
    
    monitor = PerformanceMonitor(log_file=args.log)
    monitor.watch_log()


if __name__ == "__main__":
    main()

