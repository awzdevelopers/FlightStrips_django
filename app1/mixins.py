from django.http import JsonResponse


class AjaxFormMixin(object):
    def form_invalid(self,form):
        response=super(AjaxFormMixin,self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors,staus=400)
    def form_valid(self,form):
        response=super(AjaxFormMixin,self).form_valid(form)
        if self.request.is_ajax():
            data={"message","successfully added"}
            return JsonResponse(data)
        else:
            return response
