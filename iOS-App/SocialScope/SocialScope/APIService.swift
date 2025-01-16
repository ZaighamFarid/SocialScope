//
//  APIService.swift
//  SocialScope
//
//  Handles all network requests to the backend
//

import Foundation

// Protocol so we can easily swap between real and mock implementations
protocol AnalysisServiceProtocol {
    func analyzeURL(_ url: String) async throws -> AnalysisResponse
}

// Real API service that talks to the backend
class APIService: AnalysisServiceProtocol {
    private let baseURL = "http://localhost:8000"
    
    func analyzeURL(_ url: String) async throws -> AnalysisResponse {
        guard let apiURL = URL(string: "\(baseURL)/analyze") else {
            throw APIError.invalidURL
        }
        
        var request = URLRequest(url: apiURL)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: Any] = ["url": url]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }
        
        guard httpResponse.statusCode == 200 else {
            throw APIError.serverError(statusCode: httpResponse.statusCode)
        }
        
        let decoder = JSONDecoder()
        return try decoder.decode(AnalysisResponse.self, from: data)
    }
}

// Mock service for offline demo mode - returns fake data instantly
class MockAnalysisService: AnalysisServiceProtocol {
    func analyzeURL(_ url: String) async throws -> AnalysisResponse {
        // Simulate network delay so it feels real
        try await Task.sleep(nanoseconds: 1_500_000_000) // 1.5 seconds
        
        return AnalysisResponse(
            url: url,
            platform: "Demo",
            summary: "This is a demo analysis! In real mode, I'd analyze the actual content and give you a smart summary. I'd break down the key points, tell you what people are saying, and help you craft the perfect response. Pretty cool, right?",
            sentiment: Sentiment(
                overall: "Positive",
                confidence: 0.87
            ),
            keyTopics: [
                "Demo Mode",
                "AI Analysis",
                "Social Media",
                "Smart Summaries",
                "Engagement"
            ],
            suggestedComments: SuggestedComments(
                professional: "Great insights here. I particularly appreciate the thorough analysis and well-structured approach. Looking forward to seeing more content like this.",
                friendly: "Hey, this is awesome! Really enjoyed reading through this. Thanks for sharing, definitely going to check out more of your stuff! 😊",
                funny: "Okay but who else read this three times and still wants more? Just me? No? Okay cool. 10/10 would recommend to literally everyone I know 😄",
                supportive: "You're doing amazing work! Keep it up, the effort you put into this really shows. Can't wait to see what you create next! 🙌"
            )
        )
    }
}

// Custom errors for better error handling
enum APIError: LocalizedError {
    case invalidURL
    case invalidResponse
    case serverError(statusCode: Int)
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "The URL provided is not valid"
        case .invalidResponse:
            return "Invalid response from server"
        case .serverError(let code):
            return "Server error: \(code)"
        }
    }
}
