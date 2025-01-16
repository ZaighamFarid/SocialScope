//
//  Models.swift
//  SocialScope
//
//  Data models for the app
//

import Foundation

// Main response from the backend API
struct AnalysisResponse: Codable {
    let url: String
    let platform: String
    let summary: String
    let sentiment: Sentiment
    let keyTopics: [String]
    let suggestedComments: SuggestedComments
    
    // Making keys match the backend's snake_case format
    enum CodingKeys: String, CodingKey {
        case url
        case platform
        case summary
        case sentiment
        case keyTopics = "key_topics"
        case suggestedComments = "suggested_comments"
    }
}

// Sentiment breakdown from the post
struct Sentiment: Codable {
    let overall: String
    let confidence: Double
}

// Different tones of comments the AI generates
struct SuggestedComments: Codable {
    let professional: String
    let friendly: String
    let funny: String
    let supportive: String
}

// Just the available tones as an enum for easier handling
enum CommentTone: String, CaseIterable {
    case professional = "Professional"
    case friendly = "Friendly"
    case funny = "Funny"
    case supportive = "Supportive"
    
    var emoji: String {
        switch self {
        case .professional: return "💼"
        case .friendly: return "😊"
        case .funny: return "😄"
        case .supportive: return "🤝"
        }
    }
    
    var color: String {
        switch self {
        case .professional: return "blue"
        case .friendly: return "green"
        case .funny: return "yellow"
        case .supportive: return "purple"
        }
    }
}
