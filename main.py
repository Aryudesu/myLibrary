from excelMapper.excelMapper import ExcelMapper

em = ExcelMapper("testData.xlsx", newOpenAble=True)
em.setValue(0, 0, "test")
em.saveData("testData_Output.xlsx")
print(em.getValue(0, 0))
