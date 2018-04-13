import re

# Example input: "2Y-10M-12Ds old (Apr.11, 2018)"
def format_date(arg):
    
    # extract date from round brackets
    # ['2Y', '10M', '12Ds', 'old', 'Apr', '11', '2018', '']
    tmp_list = re.split('\W+', arg)
    
    months = {  "Jan" : "01",
                "Feb" : "02",
                "Mar" : "03",
                "Apr" : "04",
                "May" : "05",
                "June" : "06",
                "July" : "07",
                "Aug." : "08",
                "Sept" : "09",
                "Oct" : "10",
                "Nov" : "11",
                "Dec" : "12" }
    
    return tmp_list[-3] + "." + months[tmp_list[-4]] + "." + tmp_list[-2]