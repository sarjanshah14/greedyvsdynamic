import time
from flask import Flask, render_template, request

app = Flask(__name__)

def get_min_coins_greedy(amount, coins):
    """
    Greedy algorithm with structured step tracking.
    """
    coins = sorted(coins, reverse=True)
    result_coins = []
    total_count = 0
    remaining = amount
    steps = []
    
    # Initial Step
    steps.append({
        'type': 'start',
        'desc': f"Starting Greedy search",
        'remaining': amount,
        'coin': None
    })
    
    for coin in coins:
        if remaining == 0:
            break
            
        steps.append({
            'type': 'check',
            'desc': f"Checking coin {coin}",
            'remaining': remaining,
            'coin': coin
        })
        
        count = remaining // coin
        if count > 0:
            result_coins.extend([coin] * count)
            remaining -= coin * count
            total_count += count
            steps.append({
                'type': 'take',
                'desc': f"Took {count}x {coin}",
                'remaining': remaining,
                'coin': coin,
                'count': count
            })
        else:
            steps.append({
                'type': 'skip',
                'desc': f"Coin {coin} > Remaining",
                'remaining': remaining,
                'coin': coin
            })
            
    if remaining != 0:
        steps.append({
            'type': 'fail',
            'desc': "Failed to reach 0",
            'remaining': remaining,
            'coin': None
        })
        return None, 0, False, steps
        
    steps.append({
        'type': 'success',
        'desc': f"Solved! Used {total_count} coins",
        'remaining': 0,
        'coin': None
    })
    return result_coins, total_count, True, steps

def get_min_coins_dp(amount, coins):
    """
    DP algorithm with structured step tracking (reconstruction).
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    parent = [-1] * (amount + 1)
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                if dp[i - coin] + 1 < dp[i]:
                    dp[i] = dp[i - coin] + 1
                    parent[i] = coin
                    
    if dp[amount] == float('inf'):
        return None, 0, False, [{'type': 'fail', 'desc': "DP Failed", 'remaining': amount}]
        
    # Reconstruct
    result_coins = []
    curr = amount
    steps = []
    steps.append({
        'type': 'start',
        'desc': f"Backtracking optimally from {amount}",
        'remaining': amount,
        'coin': None
    })
    
    while curr > 0:
        coin = parent[curr]
        result_coins.append(coin)
        curr -= coin
        steps.append({
            'type': 'take',
            'desc': f"Optimal choice: {coin}",
            'remaining': curr,
            'coin': coin
        })
        
    steps.append({
        'type': 'success',
        'desc': f"Solved! Used {len(result_coins)} coins",
        'remaining': 0,
        'coin': None
    })
    return result_coins, dp[amount], True, steps

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/team')
def team():
    return render_template('team.html')

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
