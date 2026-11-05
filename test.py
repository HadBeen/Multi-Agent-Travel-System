from tools.tavily_tool import tavily_search
from tools.flight_tool import  search_flights

res = tavily_search("hotels in algeria")
print(res)

res = search_flights('plan a 3 weeks china trip from france ')

print(res)