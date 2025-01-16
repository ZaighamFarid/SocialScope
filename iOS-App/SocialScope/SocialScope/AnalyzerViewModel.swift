//
//  AnalyzerViewModel.swift
//  SocialScope
//
//  The brain of the app - handles business logic and state
//

import Foundation
import SwiftUI
import Combine

// Following MVVM pattern - this is the ViewModel
@MainActor
class AnalyzerViewModel: ObservableObject {
    // UI state that the view observes
    @Published var urlInput: String = ""
    @Published var analysisResult: AnalysisResponse?
    @Published var isLoading: Bool = false
    @Published var errorMessage: String?
    @Published var showError: Bool = false
    @Published var selectedTone: CommentTone = .professional
    
    private var apiService: AnalysisServiceProtocol
    
    // Dependency injection - we can swap services for offline mode
    init(apiService: AnalysisServiceProtocol = APIService()) {
        self.apiService = apiService
    }
    
    // Switch between real API and mock data
    func toggleOfflineMode(_ enabled: Bool) {
        apiService = enabled ? MockAnalysisService() : APIService()
    }
    
    // Main action - analyze a URL
    func analyzeURL() async {
        // Validate the URL first
        guard !urlInput.isEmpty else {
            showErrorAlert("Please enter a URL")
            return
        }
        
        guard isValidURL(urlInput) else {
            showErrorAlert("Please enter a valid URL")
            return
        }
        
        isLoading = true
        errorMessage = nil
        
        do {
            // Call the API and wait for results
            let result = try await apiService.analyzeURL(urlInput)
            
            // Success! Update the UI
            analysisResult = result
            
            // Give haptic feedback so user knows it worked
            UIImpactFeedbackGenerator(style: .medium).impactOccurred()
        } catch {
            // Something went wrong, show the error
            showErrorAlert(error.localizedDescription)
        }
        
        isLoading = false
    }
    
    // Get the comment for the currently selected tone
    var currentComment: String {
        guard let comments = analysisResult?.suggestedComments else {
            return ""
        }
        
        switch selectedTone {
        case .professional:
            return comments.professional
        case .friendly:
            return comments.friendly
        case .funny:
            return comments.funny
        case .supportive:
            return comments.supportive
        }
    }
    
    // Copy comment to clipboard - handy for pasting into social media
    func copyComment(_ comment: String) {
        UIPasteboard.general.string = comment
        UINotificationFeedbackGenerator().notificationOccurred(.success)
    }
    
    // Clear everything and start fresh
    func reset() {
        urlInput = ""
        analysisResult = nil
        errorMessage = nil
        selectedTone = .professional
    }
    
    // Helper to show errors
    private func showErrorAlert(_ message: String) {
        errorMessage = message
        showError = true
    }
    
    // Basic URL validation
    private func isValidURL(_ string: String) -> Bool {
        guard let url = URL(string: string) else { return false }
        return url.scheme != nil && url.host != nil
    }
}
