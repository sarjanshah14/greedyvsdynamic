import time
from flask import Flask, render_template, request

app = Flask(__name__)

def get_min_coins_greedy(amount, coins):
    """
    Greedy algorithm with step tracking.
    """
    coins = sorted(coins, reverse=True)
    result_coins = []
    total_count = 0
    remaining = amount
    steps = []
    
    steps.append(f"Starting Greedy with amount: {amount}")
    steps.append(f"Sorted coins: {coins}")
    
    for coin in coins:
        if remaining == 0:
            break
        steps.append(f"Checking coin: {coin} against remaining: {remaining}")
        count = remaining // coin
        if count > 0:
            result_coins.extend([coin] * count)
            remaining -= coin * count
            total_count += count
            steps.append(f"-> Took {count}x {coin} coin(s). Remaining: {remaining}")
        else:
            steps.append(f"-> Coin {coin} is too large. Skipping.")
            
    if remaining != 0:
        steps.append("Failed to form the total amount.")
        return None, 0, False, steps
        
    steps.append(f"Success! Total coins used: {total_count}")
    return result_coins, total_count, True, steps

def get_min_coins_dp(amount, coins):
    """
    DP algorithm with step tracking (reconstruction).
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    parent = [-1] * (amount + 1)
    
    # We won't log every single DP table update as it's too much for large N.
    # We will log the reconstruction phase.
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                if dp[i - coin] + 1 < dp[i]:
                    dp[i] = dp[i - coin] + 1
                    parent[i] = coin
                    
    if dp[amount] == float('inf'):
        return None, 0, False, ["DP failed to find a solution."]
        
    # Reconstruct
    result_coins = []
    curr = amount
    steps = []
    steps.append(f"DP Table built. Reconstructing solution for amount: {amount}")
    
    while curr > 0:
        coin = parent[curr]
        result_coins.append(coin)
        prev = curr
        curr -= coin
        steps.append(f"At {prev}, best coin to take is {coin}. Remaining: {curr}")
        
    steps.append(f"Success! Total coins found: {len(result_coins)}")
    return result_coins, dp[amount], True, steps

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
        greedy_result, greedy_count, greedy_success, greedy_steps = get_min_coins_greedy(amount, coins)
        end_greedy = time.time()
        greedy_time = (end_greedy - start_greedy) * 1000  # ms
        
        # DP Execution
        start_dp = time.time()
        dp_result, dp_count, dp_success, dp_steps = get_min_coins_dp(amount, coins)
        end_dp = time.time()
        dp_time = (end_dp - start_dp) * 1000 # ms
        
        return render_template('result.html', 
                               amount=amount,
                               coins=coins,
                               greedy_result=greedy_result,
                               greedy_count=greedy_count,
                               greedy_success=greedy_success,
                               greedy_time=f"{greedy_time:.4f}",
                               greedy_steps=greedy_steps,
                               dp_result=dp_result,
                               dp_count=dp_count,
                               dp_success=dp_success,
                               dp_time=f"{dp_time:.4f}",
                               dp_steps=dp_steps)
                               
    except ValueError:
        return "Invalid input. Please enter numbers correctly.", 400

if __name__ == '__main__':
    app.run(debug=True)
