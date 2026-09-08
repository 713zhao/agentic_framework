"""Simple test to check Ollama connectivity and model responses."""

from litellm import completion

def test_ollama_model(model_name):
    """Test a specific Ollama model."""
    print(f"\n{'='*60}")
    print(f"Testing: {model_name}")
    print('='*60)
    
    try:
        # Simple test without function calling
        response = completion(
            model=f"ollama/{model_name}",
            messages=[{"role": "user", "content": "What is 2+2? Answer in one sentence."}],
            api_base="http://localhost:11434"
        )
        print(f"✓ Simple completion works!")
        print(f"Response: {response.choices[0].message.content}\n")
        
        # Test with function calling
        tools = [{
            "type": "function",
            "function": {
                "name": "get_answer",
                "description": "Get the answer to a math question",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "answer": {"type": "number", "description": "The answer"}
                    },
                    "required": ["answer"]
                }
            }
        }]
        
        response_with_tools = completion(
            model=f"ollama/{model_name}",
            messages=[{"role": "user", "content": "What is 2+2?"}],
            tools=tools,
            api_base="http://localhost:11434"
        )
        
        if response_with_tools.choices[0].message.tool_calls:
            print(f"✓ Function calling supported!")
            tool_call = response_with_tools.choices[0].message.tool_calls[0]
            print(f"Tool called: {tool_call.function.name}")
            print(f"Arguments: {tool_call.function.arguments}")
        else:
            print(f"✗ Function calling NOT supported")
            print(f"Response: {response_with_tools.choices[0].message.content}")
            
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Ollama Model Function Calling Test")
    print("="*60)
    
    # Test available models
    models_to_test = [
        "gemma2:2b-text-q8_0",
        "qwen3:1.7b",
        "gemma3:1b",
        "phi3:3.8b-mini-128k-instruct-q4_0",
        "mistral:7b-instruct-v0.2-q4_K_M",
    ]
    
    for model in models_to_test:
        test_ollama_model(model)
    
    print("\n" + "="*60)
    print("Summary:")
    print("Models that support function calling work with the agent.")
    print("Models without function calling may give errors.")
    print("="*60 + "\n")
