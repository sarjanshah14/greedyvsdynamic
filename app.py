import time
from flask import Flask, render_template, request

app = Flask(__name__)

def get_min_coins_greedy(amount, coins):
    """
    Greedy algorithm to find minimum coins.
    Sorts coins in descending order and takes the largest possible at each step.
    """
    coins = sorted(coins, reverse=True)
    result_coins = []
    total_count = 0
    remaining = amount
    
    for coin in coins:
        if remaining == 0:
            break
        count = remaining // coin
        if count > 0:
            result_coins.extend([coin] * count)
            remaining -= coin * count
            total_count += count
            
    # Check if we successfully formed the amount
    if remaining != 0:
        return None, 0, False  # Failed to form amount
        
    return result_coins, total_count, True

def get_min_coins_dp(amount, coins):
    """
    Dynamic Programming algorithm to find minimum coins.
    Guarantees optimal solution.
    """
    # dp[i] stores the minimum coins needed for amount i
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    # parent[i] stores the coin used to reach amount i (to reconstruct solution)
    parent = [-1] * (amount + 1)
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                if dp[i - coin] + 1 < dp[i]:
                    dp[i] = dp[i - coin] + 1
                    parent[i] = coin
                    
    if dp[amount] == float('inf'):
        return None, 0, False
        
    # Reconstruct the solution
    result_coins = []
    curr = amount
    while curr > 0:
        coin = parent[curr]
        result_coins.append(coin)
        curr -= coin
        
    return result_coins, dp[amount], True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    try:
        amount = int(request.form.get('amount'))
        coins_str = request.form.get('coins')
        coins = [int(c.strip()) for c in coins_str.split(',')]
        
        # Greedy Execution
        start_greedy = time.time()
        greedy_result, greedy_count, greedy_success = get_min_coins_greedy(amount, coins)
        end_greedy = time.time()
        greedy_time = (end_greedy - start_greedy) * 1000  # ms
        
        # DP Execution
        start_dp = time.time()
        dp_result, dp_count, dp_success = get_min_coins_dp(amount, coins)
        end_dp = time.time()
        dp_time = (end_dp - start_dp) * 1000 # ms
        
        return render_template('result.html', 
                               amount=amount,
                               coins=coins,
                               greedy_result=greedy_result,
                               greedy_count=greedy_count,
                               greedy_success=greedy_success,
                               greedy_time=f"{greedy_time:.4f}",
                               dp_result=dp_result,
                               dp_count=dp_count,
                               dp_success=dp_success,
                               dp_time=f"{dp_time:.4f}")
                               
    except ValueError:
        return "Invalid input. Please enter numbers correctly.", 400

if __name__ == '__main__':
    app.run(debug=True)
