def trade_checker(trade, rules):
    for rule in rules:
        comp_obj = compile(rule.code, '<string>', 'exec')
        ns = {}
        exec comp_obj in ns        
        passed = ns['check'](trade)
        if not passed:
            return False
    return True
    
