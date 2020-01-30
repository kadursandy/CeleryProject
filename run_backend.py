from tasks_backend import *

aid = reverse.delay('SANDEEP')
print(aid)
print(aid.ready())
print(aid.get())
# aid = reverse.apply_async(args=['learning celery'])