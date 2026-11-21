using System.IO.Pipes;
using System.Text;
using System.Text.Json;

namespace Mm2.Executor;

internal static class Program
{
    private const string PipeName = "mm2_executor";

    static async Task Main()
    {
        Console.WriteLine("[mm2-executor] listening on \\\\.\\pipe\\" + PipeName);
        using var server = new NamedPipeServerStream(PipeName, PipeDirection.InOut, 1,
            PipeTransmissionMode.Byte, PipeOptions.Asynchronous);
        await server.WaitForConnectionAsync();

        var reader = new StreamReader(server, Encoding.UTF8);
        var writer = new StreamWriter(server, Encoding.UTF8) { AutoFlush = true };

        while (server.IsConnected)
        {
            var line = await reader.ReadLineAsync();
            if (line is null) break;
            using var doc = JsonDocument.Parse(line);
            var op = doc.RootElement.GetProperty("op").GetString();

            if (op == "inject")
            {
                var src = doc.RootElement.GetProperty("src").GetString() ?? "";
                Console.WriteLine($"[mm2-executor] injecting {src.Length} bytes");
                await writer.WriteLineAsync("{\"ok\":true}");
            }
            else
            {
                await writer.WriteLineAsync("{\"ok\":false,\"error\":\"unknown op\"}");
            }
        }
    }
}