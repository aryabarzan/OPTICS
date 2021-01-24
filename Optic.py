import math;

#---------------------- Class Point ----------------------------
class Point:
    def __init__(self,x,y,classNumber):
        self.x=x;
        self.y=y;
        self.classNumber=classNumber;
        self.clusterNumber=0;
        self.reachability_distance=None;
        self.core_distance=None;
        self.processed=False;
    def setX(self,x):
        self.x=x;
    def setY(self,y):
        self.y=y;
    def setClusterNumber(self,clusterNumber):
        self.clusterNumber=clusterNumber;
    def setClassNumber(self,classNumber):
        self.classNumber=classNumber;
    def setReachability_distance(self,reachability_distance):
        self.reachability_distance=reachability_distance;
    def setCore_distance(self,core_distance):
        self.core_distance=core_distance;
    def setCoreDistance(self,dataset,epsilone,minpts):
        neighborsDistance=[];
        for p in dataset:
            d=self.distanceTo(p);
            if(d<=epsilone):
                neighborsDistance.append(d);

        if (len(neighborsDistance)>=minpts):
           neighborsDistance.sort();
           self.core_distance=neighborsDistance[minpts];


    def setProcessed(self,processed):
        self.processed=processed;
    def getX(self):
        return self.x;
    def getY(self):
        return self.y;
    def getClusterNumber(self):
        return self.clusterNumber;
    def getClassNumber(self):
        return self.classNumber;

    def getReachability_distance(self):
        return self.reachability_distance;
    def getCore_distance(self):
        return self.core_distance;
    def getProcessed(self):
        return self.processed;
    def distanceTo(self,to):
        return math.sqrt(math.pow(self.getX() -to.getX(), 2)+math.pow(self.getY() -to.getY(), 2));
    def getNeighboresEpsilone(self,epsilone,dataset):
    #Direct Density Reachible
        neighbors=[];
        for p in dataset:
            if(self.distanceTo(p)<=epsilone):
                neighbors.append(p);

        return neighbors;
    
    def printPoint(self):
        print '(',self.getX(),',',self.getY(),')->',self.getReachability_distance(),'-->',self.getProcessed(),'cd',self.getCore_distance(),'ccclass',self.getClassNumber();
#---------------------- End Class Point ---------------------------

#====================== Functions ========================================

def readDataSet(inputFileName):
    fin=open(inputFileName,"r");
    dataSet=[];

    for line in fin: # read rest of lines
        v=line.split();
        x=float(v[0]);
        y=float(v[1]);
        classNumber=int(v[2])
        p=Point(x,y,classNumber);
        dataSet.append(p);


    fin.close();
    return dataSet;
#---------------------------------------------------------------------

def OPTICS(Objects, e, MinPts, OrderedPoints):
    orderSeeds=[];
    for obj in objects:
        if (obj.getProcessed()==False):
            obj.setProcessed(True);
            neighbors = obj.getNeighboresEpsilone(e,Objects);
            obj.setCoreDistance(Objects,e,MinPts);
            obj.setReachability_distance(obj.getCore_distance())
            OrderedPoints.append(obj);
            if (obj.getCore_distance() != None):
                d=obj.getCore_distance();
                for  n1 in neighbors:
                    if(n1.getProcessed()==False):
                        newReachDist=max(d,n1.distanceTo(obj))
                        if(n1.getReachability_distance() == None):
                            n1.setReachability_distance(newReachDist)
                            orderSeeds.append(n1)
                        elif(n1.getReachability_distance()>newReachDist):
                            n1.setReachability_distance(newReachDist)
                 #sort orderSeeds
                for i in range(len(orderSeeds)):
                    for j in range(len(orderSeeds)-1):
                         if(orderSeeds[j].getReachability_distance()>orderSeeds[j+1].getReachability_distance()):
                            temp=orderSeeds[j];
                            orderSeeds[j]=orderSeeds[j+1]
                            orderSeeds[j+1]=temp
                while(len(orderSeeds)!=0):
                    obj1=orderSeeds[0]
                    orderSeeds.remove(obj1)
                    neighbors = obj1.getNeighboresEpsilone(e,Objects);
                    obj1.setCoreDistance(Objects,e,MinPts);
                    obj1.setProcessed(True)
                    OrderedPoints.append(obj1);
                    if (obj1.getCore_distance() != None):
                        d=obj1.getCore_distance();
                        for  n1 in neighbors:
                            newReachDist=max(d,n1.distanceTo(obj1))
                            if(n1.getReachability_distance() == None):
                                n1.setReachability_distance(newReachDist)
                                orderSeeds.append(n1)
                            elif(n1.getReachability_distance()>newReachDist):
                                n1.setReachability_distance(newReachDist)
                        #sort orderSeeds
                        for i in range(len(orderSeeds)):
                            for j in range(len(orderSeeds)-1):
                                if(orderSeeds[j].getReachability_distance()>orderSeeds[j+1].getReachability_distance()):
                                    temp=orderSeeds[j];
                                    orderSeeds[j]=orderSeeds[j+1]
                                    orderSeeds[j+1]=temp

#---------------------------------------------------------------------
def writeOrderedPointsToFile(OrderedPoints,outputFileName):
    fout=open(outputFileName,'w')
    for point in OrderedPoints:
        fout.write(str(point.getX()) +' '+str(point.getY()) + ' '+str(point.getClassNumber())+' '+str(point.getReachability_distance())+'\n' )
    fout.close()
#---------------------------------------------------------------------
#====================== End of Functions =================================

MinPts=4
e= float("infinity")
inputFileNames=['2d-2c-norm','2d-4c-no9','2d-4c-norm','myDataSet']
for inputFileName in inputFileNames:
    objects=readDataSet(inputFileName+".dat");
    OrderedPoints=[];
    OPTICS(objects, e, MinPts, OrderedPoints);
    #writeOrderedPointsToFile(OrderedPoints, inputFileName+".ord")
    