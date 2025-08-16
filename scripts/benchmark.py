#!/usr/bin/env python3
"""
QuantumChoices - Performance Benchmark Suite
Misura performance del sistema
"""

import time
import asyncio
import aiohttp
import statistics
import json
from datetime import datetime
import subprocess

class QuantumBenchmark:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
        self.results = {}
    
    async def benchmark_page_load(self, pages=None):
        """Benchmark caricamento pagine"""
        if pages is None:
            pages = ['/', '/admin', '/health']
        
        print("⚡ Benchmarking page load times...")
        
        async with aiohttp.ClientSession() as session:
            for page in pages:
                url = f"{self.base_url}{page}"
                times = []
                
                for i in range(10):  # 10 tests per page
                    start_time = time.time()
                    try:
                        async with session.get(url) as response:
                            await response.text()
                        load_time = time.time() - start_time
                        times.append(load_time)
                    except Exception as e:
                        print(f"   ❌ Failed to load {page}: {e}")
                        times.append(10.0)  # Penalty time
                
                if times:
                    avg_time = statistics.mean(times)
                    min_time = min(times)
                    max_time = max(times)
                    
                    print(f"   📄 {page}: {avg_time:.2f}s avg (min: {min_time:.2f}s, max: {max_time:.2f}s)")
                    
                    self.results[f'page_load_{page.replace("/", "_")}'] = {
                        'average': avg_time,
                        'min': min_time,
                        'max': max_time,
                        'samples': len(times)
                    }
    
    async def benchmark_api_endpoints(self):
        """Benchmark API performance"""
        print("🔌 Benchmarking API endpoints...")
        
        endpoints = [
            '/assets/data/quantum_data.json',
            '/assets/data/health_report.json'
        ]
        
        async with aiohttp.ClientSession() as session:
            for endpoint in endpoints:
                url = f"{self.base_url}{endpoint}"
                times = []
                
                for i in range(20):  # 20 tests per endpoint
                    start_time = time.time()
                    try:
                        async with session.get(url) as response:
                            data = await response.json()
                        load_time = time.time() - start_time
                        times.append(load_time)
                    except Exception as e:
                        print(f"   ❌ Failed to load {endpoint}: {e}")
                        times.append(5.0)
                
                if times:
                    avg_time = statistics.mean(times)
                    p95_time = statistics.quantiles(times, n=20)[18]  # 95th percentile
                    
                    print(f"   🔗 {endpoint}: {avg_time:.3f}s avg, {p95_time:.3f}s p95")
                    
                    self.results[f'api_{endpoint.split("/")[-1]}'] = {
                        'average': avg_time,
                        'p95': p95_time,
                        'samples': len(times)
                    }
    
    def benchmark_ai_processing(self):
        """Benchmark AI processing speed"""
        print("🤖 Benchmarking AI processing...")
        
        # Simula AI processing
        start_time = time.time()
        
        # Mock AI operations
        for i in range(100):
            # Simula calcolo Quantum Score
            score = self.mock_quantum_calculation()
        
        ai_time = time.time() - start_time
        throughput = 100 / ai_time
        
        print(f"   🧠 AI Processing: {ai_time:.2f}s for 100 products ({throughput:.1f} products/sec)")
        
        self.results['ai_processing'] = {
            'time_for_100': ai_time,
            'throughput': throughput
        }
    
    def mock_quantum_calculation(self):
        """Mock quantum score calculation"""
        # Simula calcoli complessi
        import math
        result = 0
        for i in range(1000):
            result += math.sqrt(i) * math.log(i + 1)
        return result % 10
    
    def benchmark_memory_usage(self):
        """Benchmark utilizzo memoria"""
        print("💾 Benchmarking memory usage...")
        
        try:
            import psutil
            process = psutil.Process()
            
            # Memoria iniziale
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Simula carico di lavoro
            data = []
            for i in range(10000):
                data.append({'id': i, 'data': f'test_data_{i}' * 100})
            
            # Memoria dopo carico
            loaded_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            memory_increase = loaded_memory - initial_memory
            
            print(f"   📊 Memory: {initial_memory:.1f}MB initial, {loaded_memory:.1f}MB loaded (+{memory_increase:.1f}MB)")
            
            # Cleanup
            del data
            
            self.results['memory_usage'] = {
                'initial_mb': initial_memory,
                'loaded_mb': loaded_memory,
                'increase_mb': memory_increase
            }
            
        except ImportError:
            print("   ⚠️ psutil not available, skipping memory benchmark")
    
    def benchmark_file_operations(self):
        """Benchmark operazioni file"""
        print("📁 Benchmarking file operations...")
        
        # Write benchmark
        write_times = []
        for i in range(100):
            start_time = time.time()
            with open(f'temp/benchmark_write_{i}.json', 'w') as f:
                json.dump({'test': i, 'data': 'x' * 1000}, f)
            write_times.append(time.time() - start_time)
        
        # Read benchmark
        read_times = []
        for i in range(100):
            start_time = time.time()
            with open(f'temp/benchmark_write_{i}.json', 'r') as f:
                data = json.load(f)
            read_times.append(time.time() - start_time)
        
        # Cleanup
        for i in range(100):
            try:
                import os
                os.remove(f'temp/benchmark_write_{i}.json')
            except:
                pass
        
        avg_write = statistics.mean(write_times)
        avg_read = statistics.mean(read_times)
        
        print(f"   ✍️ File Write: {avg_write:.4f}s avg")
        print(f"   📖 File Read: {avg_read:.4f}s avg")
        
        self.results['file_operations'] = {
            'write_avg': avg_write,
            'read_avg': avg_read,
            'samples': 100
        }
    
    def run_lighthouse_benchmark(self):
        """Esegue benchmark Lighthouse"""
        print("🚨 Running Lighthouse benchmark...")
        
        try:
            # Lighthouse via CLI (se disponibile)
            result = subprocess.run([
                'lighthouse', 
                self.base_url,
                '--output=json',
                '--chrome-flags="--headless"',
                '--quiet'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                lighthouse_data = json.loads(result.stdout)
                scores = lighthouse_data['lhr']['categories']
                
                lighthouse_results = {}
                for category, data in scores.items():
                    score = data['score'] * 100 if data['score'] else 0
                    lighthouse_results[category] = score
                    print(f"   🎯 {category.title()}: {score}")
                
                self.results['lighthouse'] = lighthouse_results
            else:
                print("   ⚠️ Lighthouse failed to run")
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("   ⚠️ Lighthouse not available")
    
    async def run_full_benchmark(self):
        """Esegue benchmark completo"""
        print("🏁 Starting QuantumChoices Performance Benchmark")
        print("=" * 60)
        
        # Assicura che temp directory esista
        import os
        os.makedirs('temp', exist_ok=True)
        
        benchmarks = [
            ("Page Load Performance", self.benchmark_page_load()),
            ("API Endpoints", self.benchmark_api_endpoints()),
            ("AI Processing", self.benchmark_ai_processing),
            ("Memory Usage", self.benchmark_memory_usage),
            ("File Operations", self.benchmark_file_operations),
            ("Lighthouse Audit", self.run_lighthouse_benchmark)
        ]
        
        for name, benchmark in benchmarks:
            print(f"\n🔬 {name}")
            print("-" * 40)
            
            try:
                if asyncio.iscoroutine(benchmark):
                    await benchmark
                else:
                    benchmark()
            except Exception as e:
                print(f"   ❌ {name} failed: {e}")
        
        # Salva risultati
        self.save_benchmark_results()
        
        # Summary
        self.print_summary()
    
    def save_benchmark_results(self):
        """Salva risultati benchmark"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'benchmark_results_{timestamp}.json'
        
        results_with_metadata = {
            'timestamp': datetime.now().isoformat(),
            'base_url': self.base_url,
            'results': self.results
        }
        
        with open(filename, 'w') as f:
            json.dump(results_with_metadata, f, indent=2)
        
        print(f"\n💾 Results saved to: {filename}")
    
    def print_summary(self):
        """Stampa summary risultati"""
        print("\n" + "=" * 60)
        print("📊 BENCHMARK SUMMARY")
        print("=" * 60)
        
        # Performance scores
        page_load_avg = self.results.get('page_load__', {}).get('average', 0)
        if page_load_avg:
            if page_load_avg < 1.0:
                print("⚡ Page Load: EXCELLENT (<1s)")
            elif page_load_avg < 2.0:
                print("✅ Page Load: GOOD (<2s)")
            elif page_load_avg < 3.0:
                print("⚠️ Page Load: FAIR (<3s)")
            else:
                print("❌ Page Load: POOR (>3s)")
        
        # AI throughput
        ai_throughput = self.results.get('ai_processing', {}).get('throughput', 0)
        if ai_throughput:
            print(f"🤖 AI Throughput: {ai_throughput:.1f} products/sec")
        
        # Memory efficiency
        memory_increase = self.results.get('memory_usage', {}).get('increase_mb', 0)
        if memory_increase:
            if memory_increase < 50:
                print("💾 Memory Usage: EFFICIENT (<50MB increase)")
            elif memory_increase < 100:
                print("⚠️ Memory Usage: MODERATE (<100MB increase)")
            else:
                print("❌ Memory Usage: HIGH (>100MB increase)")
        
        # Lighthouse scores
        lighthouse = self.results.get('lighthouse', {})
        if lighthouse:
            avg_lighthouse = sum(lighthouse.values()) / len(lighthouse)
            if avg_lighthouse >= 90:
                print(f"🚨 Lighthouse: EXCELLENT ({avg_lighthouse:.0f}/100)")
            elif avg_lighthouse >= 70:
                print(f"✅ Lighthouse: GOOD ({avg_lighthouse:.0f}/100)")
            else:
                print(f"⚠️ Lighthouse: NEEDS IMPROVEMENT ({avg_lighthouse:.0f}/100)")
        
        print("\n🎯 Overall Performance: ", end="")
        
        # Calculate overall score
        scores = []
        if page_load_avg and page_load_avg < 2.0:
            scores.append(1)
        if ai_throughput and ai_throughput > 50:
            scores.append(1)
        if memory_increase and memory_increase < 100:
            scores.append(1)
        if lighthouse and sum(lighthouse.values()) / len(lighthouse) >= 80:
            scores.append(1)
        
        overall_score = sum(scores) / 4 * 100 if scores else 0
        
        if overall_score >= 75:
            print("🚀 EXCELLENT")
        elif overall_score >= 50:
            print("✅ GOOD")
        else:
            print("⚠️ NEEDS OPTIMIZATION")
        
        print(f"\n📈 Performance Score: {overall_score:.0f}/100")

async def main():
    benchmark = QuantumBenchmark()
    await benchmark.run_full_benchmark()

if __name__ == "__main__":
    asyncio.run(main())
