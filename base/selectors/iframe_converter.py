def converter(url):
    url_ = url.split('reporting')
    iframe = f'{url_[0]}embed/reporting{url_[1]}'
    return iframe
    