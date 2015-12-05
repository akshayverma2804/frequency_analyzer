package com.soundanalyzer;

import java.util.List;

public class calcFrequency{
	private double eps = 0.0000001;
	
	public double getFrequency(List<Double> L, double dt){
		List<Double> pointFreq = null;
		
		for (int i=0; i+1<L.size(); i++){
			if (L.get(i)*L.get(i+1)<=0){
				if ((L.get(i+1)==0) && (i+1!=(L.size()-1))){
					continue;
				}
				double dx = dt; //?
				double dy = L.get(i+1) - L.get(i);
				double m = (dy/dx);
				double c = L.get(i) - (m*i*dt);
				double x = (c*(-1.0))/(m+eps);
				pointFreq.add(x);
			}
		}
        double avg_delta_T = 0.0;
        for (int i=0; i<pointFreq.size(); i++){
            double deltaT = 2*(pointFreq.get(i) - pointFreq.get(i-1));
            avg_delta_T += deltaT; 
        }
        
        //print "avg delta, number of zero crossings : "+str(avg_delta_T)+" , "+str(len(X))
        //print "in cur win_ zero points = "+str(len(X))
        if (pointFreq.size()<=1){
            return -1.0;
        }
        else {    
        	avg_delta_T = (avg_delta_T/((1.0)*(pointFreq.size()-1)));
        }
        double data = 1.0/(avg_delta_T+eps);
        return data;
	} 
}
