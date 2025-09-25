ObjValue=nan(100,3);
DecValue=nan(100,7);
Result=result{10,2};
for i=1:100
    ObjValue(i,:)=Result(i).obj;
    DecValue(i,:)=Result(i).dec;
end