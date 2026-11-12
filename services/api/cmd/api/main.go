package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"apex/api/internal/api"
	"apex/api/internal/content"
	"apex/api/internal/db"
)

func main() {
	logger := slog.New(slog.NewTextHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))
	ctx := context.Background()
	databaseURL := env("DATABASE_URL", "postgres://apex:apex@127.0.0.1:5433/apex?sslmode=disable")
	demoMode := env("LOCAL_DEMO_MODE", "true") == "true"
	if demoMode && env("APP_ENV", "development") == "production" {
		logger.Error("refusing to start: LOCAL_DEMO_MODE cannot be enabled in production")
		os.Exit(1)
	}
	pack, err := content.Load()
	if err != nil {
		logger.Error("load exam content", "err", err)
		os.Exit(1)
	}
	store, err := db.Open(ctx, databaseURL)
	if err != nil {
		logger.Error("connect database", "err", err)
		os.Exit(1)
	}
	defer store.Close()
	if err := store.Migrate(ctx); err != nil {
		logger.Error("migrate database", "err", err)
		os.Exit(1)
	}
	for _, exam := range pack.Exams {
		if err := store.Seed(ctx, exam); err != nil {
			logger.Error("seed database", "err", err, "exam", exam.ID)
			os.Exit(1)
		}
	}
	mediaDir := env("MEDIA_DIR", "./media")
	srv := api.New(store, pack.Exams, demoMode, mediaDir, logger)
	httpServer := &http.Server{Addr: env("API_ADDR", ":8080"), Handler: srv.Handler(), ReadHeaderTimeout: 10 * time.Second, ReadTimeout: 30 * time.Second, WriteTimeout: 60 * time.Second}
	go func() {
		logger.Info("Apex API listening", "addr", httpServer.Addr, "demoMode", demoMode)
		if err := httpServer.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.Error("server", "err", err)
			os.Exit(1)
		}
	}()
	stop := make(chan os.Signal, 1)
	signal.Notify(stop, syscall.SIGINT, syscall.SIGTERM)
	<-stop
	shutdown, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	_ = httpServer.Shutdown(shutdown)
	_ = srv.Close()
}

func env(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}
