// Art Gallery Implementation with Ada Laurent's Design Philosophy
// Context: Cultural/Art Collection with search results for "cats"
import React, { useState, useEffect } from 'react';
// import artworks from '../data/artworks.json';

const ArtGallery = () => {
  const [artworks, setArtworks] = useState([]);
  const [selectedArtwork, setSelectedArtwork] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArtworks = async () => {
      try {
        setIsLoading(true);
        const response = await fetch('https://api.artic.edu/api/v1/artworks/search?q=cats');
        const data = await response.json();
        
        if (data.data) {
          setArtworks(data.data);
        } else {
          throw new Error('No artwork data found');
        }
      } catch (err) {
        setError('Failed to load artworks. Please try again later.');
        console.error('Error fetching artworks:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchArtworks();
  }, []);

  // Ada: "Let's add some elegant loading and error states"
  if (error) {
    return (
      <div className="error-state">
        <div className="error-message">{error}</div>
      </div>
    );
  }

  const galleryStyles = `
    /* Previous styles remain the same... */

    /* Adding loading state container */
    .loading-container {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 2rem;
      padding: 2rem;
    }

    .loading-card {
      height: 400px;
      background: linear-gradient(
        90deg,
        #f0f0f0 0%,
        #f8f8f8 50%,
        #f0f0f0 100%
      );
      border-radius: 12px;
      animation: pulse 1.5s infinite;
    }

    @keyframes pulse {
      0% { opacity: 0.6; }
      50% { opacity: 1; }
      100% { opacity: 0.6; }
    }

    .error-state {
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 50vh;
      padding: 2rem;
    }

    .error-message {
      background: #fee;
      color: #c33;
      padding: 1rem 2rem;
      border-radius: 8px;
      text-align: center;
    }
  `;

  // Ada: "Show a sophisticated loading state while we fetch"
  if (isLoading) {
    return (
      <>
        <style>{galleryStyles}</style>
        <div className="loading-container">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="loading-card" />
          ))}
        </div>
      </>
    );
  }

  return (
    <>
      <style>{galleryStyles}</style>
      
      <div className="art-gallery">
        {artworks.map(artwork => (
          <div 
            key={artwork.id} 
            className="artwork-card"
            onClick={() => setSelectedArtwork(artwork)}
          >
            <div className="artwork-image">
              <img 
                src={artwork.thumbnail.lqip} 
                alt={artwork.thumbnail.alt_text}
                loading="lazy"
              />
            </div>
            <div className="artwork-details">
              <h2 className="artwork-title">{artwork.title}</h2>
              <div className="artwork-meta">
                Art Institute of Chicago
              </div>
            </div>
          </div>
        ))}
      </div>

      {selectedArtwork && (
        <div 
          className={`artwork-modal ${selectedArtwork ? 'visible' : ''}`}
          onClick={() => setSelectedArtwork(null)}
        >
          <div className="modal-content">
            <img 
              src={selectedArtwork.thumbnail.lqip} 
              alt={selectedArtwork.thumbnail.alt_text}
            />
            <div className="artwork-details">
              <h2 className="artwork-title">{selectedArtwork.title}</h2>
              <div className="artwork-meta">
                <p>{selectedArtwork.thumbnail.alt_text}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default ArtGallery;