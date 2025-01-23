from flask import Flask, render_template, request, jsonify
from sieve0 import sieve0
from sieve1 import sieve1
from sieve2 import sieve2
import time

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_sieve():
    # Change from request.form to request.json to handle JSON data
    data = request.json  # Accessing JSON data
    n = int(data["n"])   # Extracting 'n' from JSON
    algorithm = data["algorithm"]

    start_time = time.time()

    if algorithm == "sieve0":
        result = sieve0(n)
    elif algorithm == "sieve1":
        result = sieve1(n)
    elif algorithm == "sieve2":
        result = sieve2(n)
    else:
        return jsonify({"error": "Invalid algorithm selected"}), 400

    end_time = time.time()
    execution_time = end_time - start_time

    return jsonify({
        "primes_count": result,
        "execution_time": execution_time
    })

@app.route("/benchmark", methods=["POST"])
def benchmark():
    data = request.json  # Accessing JSON data for benchmark
    n = int(data["n"])
    runs_count = int(data.get("runs_count", 10))
    
    results = {}
    
    for algorithm, func in [("sieve0", sieve0), ("sieve1", sieve1), ("sieve2", sieve2)]:
        total_time = 0
        primes_count = 0
        
        for _ in range(runs_count):
            start_time = time.time()
            primes_count = func(n)
            end_time = time.time()
            total_time += (end_time - start_time)

        avg_time = total_time / runs_count
        results[algorithm] = {
            "primes_count": primes_count,
            "avg_time": avg_time
        }

    # Calculate speedups
    speedup_10 = results["sieve0"]["avg_time"] / results["sieve1"]["avg_time"]
    speedup_12 = results["sieve0"]["avg_time"] / results["sieve2"]["avg_time"]
    
    results["speedups"] = {
        "speedup_10": speedup_10,
        "speedup_12": speedup_12
    }

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
