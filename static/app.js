// iReply Frontend Application

// State
let conversations = [];
let needToReply = [];
let currentDraft = {
    chatId: null,
    recipient: null,
    message: ''
};

// DOM Elements
const statusBar = document.getElementById('status-bar');
const statusDot = statusBar.querySelector('.status-dot');
const statusText = statusBar.querySelector('.status-text');
const thresholdInput = document.getElementById('threshold-input');
const sortSelect = document.getElementById('sort-select');
const refreshBtn = document.getElementById('refresh-btn');
const conversationsContainer = document.getElementById('conversations-container');
const needReplyContainer = document.getElementById('need-reply-container');
const draftModal = document.getElementById('draft-modal');
const confirmModal = document.getElementById('confirm-modal');
const toast = document.getElementById('toast');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkHealth();
    refreshBtn.addEventListener('click', loadConversations);
    
    // Sort change - re-render
    sortSelect.addEventListener('change', () => {
        if (conversations.length > 0 || needToReply.length > 0) {
            renderNeedToReply();
            renderConversations();
        }
    });
    
    // Threshold input - reload on Enter or blur
    thresholdInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            thresholdInput.blur();
            loadConversations();
        }
    });
    
    thresholdInput.addEventListener('blur', () => {
        // Ensure value is valid
        let val = parseInt(thresholdInput.value) || 0;
        val = Math.max(0, Math.min(720, val));
        thresholdInput.value = val;
    });
});

// Sort helper
function sortConversations(convos) {
    const sorted = [...convos];
    if (sortSelect.value === 'asc') {
        sorted.sort((a, b) => a.hours_ago - b.hours_ago); // Newest first
    } else {
        sorted.sort((a, b) => b.hours_ago - a.hours_ago); // Oldest first
    }
    return sorted;
}

// API Functions
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        
        if (data.api_key_configured && data.database_accessible) {
            setStatus('connected', 'Connected');
            // Set input to server's default threshold
            thresholdInput.value = data.stale_threshold_hours;
        } else if (!data.api_key_configured) {
            setStatus('error', 'API key not configured');
        } else if (!data.database_accessible) {
            setStatus('error', 'Database not accessible');
        }
    } catch (error) {
        setStatus('error', 'Server offline');
    }
}

async function loadConversations() {
    refreshBtn.classList.add('loading');
    refreshBtn.disabled = true;
    
    const loadingHtml = `
        <div class="loading-conversations">
            <div class="loading-spinner"></div>
            <p class="loading-text">Scanning iMessage database...</p>
        </div>
    `;
    
    conversationsContainer.innerHTML = loadingHtml;
    needReplyContainer.innerHTML = loadingHtml;
    
    try {
        const threshold = thresholdInput.value;
        
        // Fetch both types in parallel
        const [staleResponse, needReplyResponse] = await Promise.all([
            fetch(`/api/conversations?threshold=${threshold}`),
            fetch(`/api/need-to-reply?threshold=${threshold}`)
        ]);
        
        if (!staleResponse.ok) {
            const error = await staleResponse.json();
            throw new Error(error.detail || 'Failed to load conversations');
        }
        
        conversations = await staleResponse.json();
        needToReply = await needReplyResponse.json();
        
        renderConversations();
        renderNeedToReply();
        
        const total = conversations.length + needToReply.length;
        if (total > 0) {
            showToast('success', `Found ${needToReply.length} to reply, ${conversations.length} waiting`);
        }
    } catch (error) {
        showToast('error', error.message);
        const errorHtml = `
            <div class="empty-state">
                <span class="empty-icon">⚠️</span>
                <p>${error.message}</p>
            </div>
        `;
        conversationsContainer.innerHTML = errorHtml;
        needReplyContainer.innerHTML = errorHtml;
    } finally {
        refreshBtn.classList.remove('loading');
        refreshBtn.disabled = false;
    }
}

async function generateDraft(chatId, contact) {
    currentDraft.chatId = chatId;
    currentDraft.recipient = contact;
    
    const draftText = document.getElementById('draft-text');
    const draftRecipient = document.getElementById('draft-recipient');
    const draftContextCount = document.getElementById('draft-context-count');
    const regenerateBtn = document.getElementById('regenerate-btn');
    const sendBtn = document.getElementById('send-btn');
    
    draftRecipient.textContent = contact;
    draftText.value = 'Generating...';
    draftText.disabled = true;
    regenerateBtn.disabled = true;
    sendBtn.disabled = true;
    
    openDraftModal();
    
    try {
        const response = await fetch('/api/generate-draft', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: chatId, contact: contact })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to generate draft');
        }
        
        const data = await response.json();
        currentDraft.message = data.draft;
        
        draftText.value = data.draft;
        draftContextCount.textContent = `${data.context_messages} messages analyzed`;
        draftText.disabled = false;
        regenerateBtn.disabled = false;
        sendBtn.disabled = false;
        
    } catch (error) {
        draftText.value = `Error: ${error.message}`;
        showToast('error', error.message);
    }
}

async function regenerateDraft() {
    if (currentDraft.chatId && currentDraft.recipient) {
        await generateDraft(currentDraft.chatId, currentDraft.recipient);
    }
}

function sendMessage() {
    const draftText = document.getElementById('draft-text');
    currentDraft.message = draftText.value;
    
    document.getElementById('confirm-recipient').textContent = currentDraft.recipient;
    openConfirmModal();
}

async function confirmSend() {
    closeConfirmModal();
    
    const sendBtn = document.getElementById('send-btn');
    sendBtn.classList.add('loading');
    sendBtn.disabled = true;
    
    try {
        const response = await fetch('/api/send-message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                recipient: currentDraft.recipient,
                message: currentDraft.message
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('success', 'Message sent successfully!');
            closeDraftModal();
            // Remove the conversation from the list
            conversations = conversations.filter(c => c.chat_id !== currentDraft.chatId);
            renderConversations();
        } else {
            showToast('error', data.error || 'Failed to send message');
        }
    } catch (error) {
        showToast('error', error.message);
    } finally {
        sendBtn.classList.remove('loading');
        sendBtn.disabled = false;
    }
}

// Render Functions
function renderNeedToReply() {
    if (needToReply.length === 0) {
        needReplyContainer.innerHTML = `
            <div class="no-results">
                <span class="no-results-icon">✨</span>
                <h3>All caught up!</h3>
                <p>No messages waiting for your reply!</p>
            </div>
        `;
        return;
    }
    
    const sorted = sortConversations(needToReply);
    needReplyContainer.innerHTML = sorted.map(conv => `
        <div class="conversation-card need-reply" data-chat-id="${conv.chat_id}" data-contact="${escapeHtml(conv.contact)}">
            <div class="card-header">
                <span class="contact-name">
                    ${conv.contact_name ? escapeHtml(conv.contact_name) : escapeHtml(conv.contact)}
                    ${conv.is_group ? '<span class="group-badge">Group</span>' : ''}
                </span>
                <span class="time-badge need-reply-badge ${conv.hours_ago > 24 ? 'urgent' : ''}">${conv.hours_ago}h</span>
            </div>
            ${conv.contact_name ? `<p class="contact-identifier">${escapeHtml(conv.contact)}</p>` : ''}
            <p class="last-message">"${escapeHtml(conv.last_message)}"</p>
            <p class="context-info">📝 ${conv.context_count} messages with context</p>
            <div class="card-actions">
                <button class="btn btn-primary generate-btn">
                    <span class="btn-icon">✨</span>
                    Generate Reply
                </button>
            </div>
        </div>
    `).join('');
    
    // Add event listeners
    needReplyContainer.querySelectorAll('.generate-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const card = this.closest('.conversation-card');
            const chatId = parseInt(card.dataset.chatId);
            const contact = card.dataset.contact;
            generateDraft(chatId, contact);
        });
    });
}

function renderConversations() {
    if (conversations.length === 0) {
        conversationsContainer.innerHTML = `
            <div class="no-results">
                <span class="no-results-icon">✨</span>
                <h3>All caught up!</h3>
                <p>No one is ghosting you!</p>
            </div>
        `;
        return;
    }
    
    const sorted = sortConversations(conversations);
    conversationsContainer.innerHTML = sorted.map(conv => `
        <div class="conversation-card" data-chat-id="${conv.chat_id}" data-contact="${escapeHtml(conv.contact)}">
            <div class="card-header">
                <span class="contact-name">
                    ${conv.contact_name ? escapeHtml(conv.contact_name) : escapeHtml(conv.contact)}
                    ${conv.is_group ? '<span class="group-badge">Group</span>' : ''}
                </span>
                <span class="time-badge ${conv.hours_ago > 72 ? 'urgent' : ''}">${conv.hours_ago}h</span>
            </div>
            ${conv.contact_name ? `<p class="contact-identifier">${escapeHtml(conv.contact)}</p>` : ''}
            <p class="last-message">"${escapeHtml(conv.last_message)}"</p>
            <p class="context-info">📝 ${conv.context_count} messages with context</p>
            <div class="card-actions">
                <button class="btn btn-primary generate-btn">
                    <span class="btn-icon">✨</span>
                    Generate Follow-up
                </button>
            </div>
        </div>
    `).join('');
    
    // Add event listeners to all generate buttons
    conversationsContainer.querySelectorAll('.generate-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const card = this.closest('.conversation-card');
            const chatId = parseInt(card.dataset.chatId);
            const contact = card.dataset.contact;
            generateDraft(chatId, contact);
        });
    });
}

// Modal Functions
function openDraftModal() {
    draftModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

function closeDraftModal() {
    draftModal.classList.add('hidden');
    document.body.style.overflow = '';
    currentDraft = { chatId: null, recipient: null, message: '' };
}

function openConfirmModal() {
    confirmModal.classList.remove('hidden');
}

function closeConfirmModal() {
    confirmModal.classList.add('hidden');
}

// Close modals on backdrop click
draftModal.querySelector('.modal-backdrop').addEventListener('click', closeDraftModal);
confirmModal.querySelector('.modal-backdrop').addEventListener('click', closeConfirmModal);

// UI Helpers
function setStatus(state, text) {
    statusDot.className = 'status-dot ' + state;
    statusText.textContent = text;
}

function showToast(type, message) {
    const toastIcon = toast.querySelector('.toast-icon');
    const toastMessage = toast.querySelector('.toast-message');
    
    toast.className = 'toast ' + type;
    toastIcon.textContent = type === 'success' ? '✓' : '✗';
    toastMessage.textContent = message;
    
    // Auto-hide after 4 seconds
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 4000);
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeDraftModal();
        closeConfirmModal();
    }
});

