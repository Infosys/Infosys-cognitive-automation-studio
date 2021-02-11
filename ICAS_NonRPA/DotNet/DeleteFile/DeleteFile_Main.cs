//Copyright 2020 Infosys Ltd.

//Use of this source code is governed by Apache 2.0 license that can be found in the LICENSE file or at https://opensource.org/licenses/Apache-2.0
using System;
using Serilog.Core;
using DotNetBotFramework;

namespace DeleteFile
{
    public class DeleteFile_Main : AbstractBot
    {
        //Implement the commented code below 

        public static Logger logger = LoggingService.LoggingServiceMethod();

        [Bot("DeleteFile", "1.0","","String","","DotNetFramework","02","01","01")]

        public override void Bot_Init()
        {
			logger.Information("Inside Init");
        }

        [NotNull]
        public string sourceFile { get; set; }

        //Error Handling Attributes
        [Error("NullReferenceException", "Null value is referenced", "02010102FF")]
        [Error("IOException", "Input Exception", "02010101FF")]
        [Error("Validation Error", "File Does Not Exist", "0201011103")]

        public override string Execute()
        {
            Console.WriteLine("In execute method");
            String error = "11";
            String errorcategorycode = "03";
            String errorcodeA = "02" + "01" + "01";
		//ErrorCode generation
            if (!System.IO.File.Exists(sourceFile))
            {
                string errorcodeB = error + errorcategorycode;
                string errorcode = errorcodeA + errorcodeB;

                outputParams.Add("Exception", "Validation Error");
                outputParams.Add("ErrorCode", errorcode);
                outputParams.Add("ErrorMessage", "File Does Not Exist");
                logger.Error("Error", outputParams);
                return "Failed Due to wrong EmailId";
            }
            

            if (System.IO.File.Exists(sourceFile))
            {
                try
                {
                    Console.WriteLine("--in  ....try block--");
                    System.IO.File.Delete(sourceFile);
                    outputParams.Add("Response", "Success");
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.Message);
                    outputParams.Add("Response", "Failure");
                }
            }
            else
            {
                Console.WriteLine("File doesnt exist");
                outputParams.Add("Response", "Failure");
            }
            return "Success Message";

        }              

    }
}
