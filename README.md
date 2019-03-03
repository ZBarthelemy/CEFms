# CEFms
Close Ended Fund monitor system. Just a service scraping published data on the web for a client down stream.

```python
>>> import pycef
>>> c = pycef.Client()
>>> f = c.get_fund_by_ticker('jps')
>>> f.current_premium_to_nav
-0.039
```
