from django.http import HttpResponse
from django.views.generic import TemplateView
import xlwt

class XLSXResponse(TemplateView):

  def render_to_response(self, generator, **response_kwargs):
      response = HttpResponse(content_type='application/ms-excel')
      response['Content-Disposition'] = 'attachment; filename=export.xls'
      wb = xlwt.Workbook(encoding='utf-8')
      ws = wb.add_sheet("data")

      for j,c in enumerate(generator['headers']):
              ws.write(0,j,c)

      for i,row in enumerate(generator):
          for j,c in enumerate(row):
              ws.write(i+1,j,c)

      wb.save(response)
      return response
        

class XLSResponse(HttpResponse):
    
    def __init__(self, data, **kwargs):
        kwargs['content_type'] = 'application/vnd.ms-excel'
        super(XLSResponse, self).__init__(data, **kwargs)