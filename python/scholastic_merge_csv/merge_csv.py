import pandas
def merge_csv(u_file, ng_file):
    print "reading u csv file:", u_file
    u_id = "student_id"
    u_data = pandas.read_csv(u_file, dtype='unicode')
    print "reading ng csv file:", ng_file
    ng_id = "USER_ID"
    ng_data = pandas.read_csv(ng_file, dtype='unicode')
    print "merging files..."
    merged = pandas.merge(u_data, ng_data, left_on=u_id, right_on=ng_id, how="outer")
    print "done"
    return (merged, ng_data.columns.append(u_data.columns)) 