def trade_checker(trade, portofolio, rules):
    for rule in rules:
        comp_obj = compile(rule.code, '<string>', 'exec')
        ns = {}
        exec comp_obj in ns        
        passed = ns['check'](trade, portofolio)
        if not passed:
            return False
    return True
    
