package com.soundanalyzer;
import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class wavreader
{
   public static void main(String[] args)
   {
      try
      {
         // Open the wav file specified as the first argument
    	 System.out.println("opening file");
         WavFile wavFile = WavFile.openWavFile(new File("/home/akshay/eclipse/workspace/SoundAnalyzer/src/com/soundanalyzer/test.wav"));
         System.out.println("file opened");
         // Display information about the wav file
         wavFile.display();

         // Get the number of audio channels in the wav file
         int numChannels = wavFile.getNumChannels();

         // Create a buffer of 100 frames
         double[] buffer = new double[100 * numChannels];

         int framesRead;
         double min = Double.MAX_VALUE;
         double max = Double.MIN_VALUE;
         double sample_rate = wavFile.getSampleRate()*1.0;
         
         System.out.print("entering calcutations\n");
         
         List<Double> freq = new ArrayList();
         
         do
         {
            // Read frames into buffer
            framesRead = wavFile.readFrames(buffer, 100);
            String ll = "";
            // Loop through frames and look for minimum and maximum value
            List<Double> datapts = new ArrayList();
            double dt = 1.0/sample_rate;
            
            for (int s=0 ; s<framesRead * numChannels ; s++)
            {
               ll += String.valueOf(buffer[s]);
               ll += " ";
               datapts.add(buffer[s]);
               //if (buffer[s] > max) max = buffer[s];
               //if (buffer[s] < min) min = buffer[s];
            }
            calcFrequency cf = new calcFrequency();
            double f = cf.getFrequency(datapts, dt);
            if (f>0.0){
            	freq.add(f);
            }
            System.out.println(ll);
         }
         while (framesRead != 0);

         // Close the wavFile
         wavFile.close();

         // Output the minimum and maximum value
         System.out.printf("Min: %f, Max: %f\n", min, max);
         
         System.out.println("Frequencies");
         
         for (int i=0; i<freq.size(); i++){
        	 System.out.printf("frame number %d, freq = %f\n", i, freq.get(i));
         }
         
      }
      catch (Exception e)
      {
         System.err.println(e);
      }
   }
}