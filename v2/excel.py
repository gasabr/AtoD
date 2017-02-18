import os
import xlsxwriter
from sqlalchemy.inspection import inspect

from models import HeroModel
import settings

mapper = inspect(HeroModel)

# Create an new Excel file and add a worksheet.
filepath = os.path.join(settings.DATA_FOLDER + 'classes.xlsx')

workbook = xlsxwriter.Workbook(filepath)
worksheet = workbook.add_worksheet()

# Widen the first column to make the text clearer.
worksheet.set_column('A:A', 20)

for i, column in enumerate(mapper.attrs):
    worksheet.write(1+i, 0, column.key)

workbook.close()
