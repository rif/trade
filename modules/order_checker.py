def order_checker(odrer, portofolio, rules):
    for rule in rules:
        comp_obj = compile(rule.code, '<string>', 'exec')
        ns = {}
        exec comp_obj in ns        
        passed = ns['check'](odrer, portofolio)
        if not passed:
            return (False, rule.name)
    return (True, 'OK')
